import codecs
from distutils.version import (
    LooseVersion,
)
import functools
import json
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Optional,
    Tuple,
    Union,
    cast,
)

import platon_abi
from platon_abi.exceptions import (
    ParseError,
)
from platon_abi.grammar import (
    BasicType,
    parse,
)
from platon_typing import (
    Bech32Address,
    HexStr,
    TypeStr, Address,
)
from platon_utils import (
    to_bytes,
    to_bech32_address,
    to_hex,
    to_text, to_canonical_address, is_address,
)
from platon_utils.toolz import (
    curry,
)
from hexbytes import (
    HexBytes,
)

from ens import ENS
from platon._utils.encoding import (
    hexstr_if_str,
    text_if_str,
)
from platon._utils.ens import (
    StaticENS,
    is_ens_name,
    validate_name_has_address,
)
from platon._utils.validation import (
    validate_abi,
    validate_address,
)
from platon.exceptions import (
    InvalidAddress,
)
from platon.types import (  # noqa: F401
    ABI,
    ABIEvent,
    ABIFunction,
)

if TYPE_CHECKING:
    from platon import Web3  # noqa: F401


def implicitly_identity(
    to_wrap: Callable[[TypeStr, Any], Any]
) -> Callable[[TypeStr, Any], Tuple[TypeStr, Any]]:
    @functools.wraps(to_wrap)
    def wrapper(type_str: TypeStr, data: Any) -> Tuple[TypeStr, Any]:
        modified = to_wrap(type_str, data)
        if modified is None:
            return type_str, data
        else:
            return modified
    return wrapper


#
# Return Normalizers
#


@implicitly_identity
def addresses_bech32(type_str: TypeStr, data: Any) -> Tuple[TypeStr, Bech32Address]:
    if type_str == 'address':
        return type_str, to_bech32_address(data)
    return None


@implicitly_identity
def decode_abi_strings(type_str: TypeStr, data: Any) -> Tuple[TypeStr, str]:
    if type_str == 'string':
        return type_str, codecs.decode(data, 'utf8', 'backslashreplace')
    return None


#
# Argument Normalizers
#


def parse_basic_type_str(
    old_normalizer: Callable[[BasicType, TypeStr, Any], Tuple[TypeStr, Any]]
) -> Callable[[TypeStr, Any], Tuple[TypeStr, Any]]:
    """
    Modifies a normalizer to automatically parse the incoming type string.  If
    that type string does not represent a basic type (i.e. non-tuple type) or is
    not parsable, the normalizer does nothing.
    """
    @functools.wraps(old_normalizer)
    def new_normalizer(type_str: TypeStr, data: Any) -> Tuple[TypeStr, Any]:
        try:
            abi_type = parse(type_str)
        except ParseError:
            # If type string is not parsable, do nothing
            return type_str, data

        if not isinstance(abi_type, BasicType):
            return type_str, data

        return old_normalizer(abi_type, type_str, data)

    return new_normalizer


@implicitly_identity
@parse_basic_type_str
def abi_bytes_to_hex(
    abi_type: BasicType, type_str: TypeStr, data: Any
) -> Optional[Tuple[TypeStr, HexStr]]:
    if abi_type.base != 'bytes' or abi_type.is_array:
        return None

    bytes_data = hexstr_if_str(to_bytes, data)
    if abi_type.sub is None:
        return type_str, to_hex(bytes_data)

    num_bytes = abi_type.sub
    if len(bytes_data) > num_bytes:
        raise ValueError(
            "This value was expected to be at most %d bytes, but instead was %d: %r" % (
                (num_bytes, len(bytes_data), data)
            )
        )

    padded = bytes_data.ljust(num_bytes, b'\0')
    return type_str, to_hex(padded)


@implicitly_identity
@parse_basic_type_str
def abi_int_to_hex(
    abi_type: BasicType, type_str: TypeStr, data: Any
) -> Optional[Tuple[TypeStr, HexStr]]:
    if abi_type.base == 'uint' and not abi_type.is_array:
        # double check?
        return type_str, hexstr_if_str(to_hex, data)
    return None


@implicitly_identity
def abi_string_to_hex(type_str: TypeStr, data: Any) -> Optional[Tuple[TypeStr, str]]:
    if type_str == 'string':
        return type_str, text_if_str(to_hex, data)
    return None


@implicitly_identity
def abi_string_to_text(type_str: TypeStr, data: Any) -> Optional[Tuple[TypeStr, str]]:
    if type_str == 'string':
        return type_str, text_if_str(to_text, data)
    return None


@implicitly_identity
@parse_basic_type_str
def abi_bytes_to_bytes(
    abi_type: BasicType, type_str: TypeStr, data: Any
) -> Optional[Tuple[TypeStr, HexStr]]:
    if abi_type.base == 'bytes' and not abi_type.is_array:
        return type_str, hexstr_if_str(to_bytes, data)
    return None


@implicitly_identity
def abi_address_to_bytes(type_str: TypeStr, data: Any) -> Optional[Tuple[TypeStr, Address]]:
    if type_str == 'address':
        validate_address(data)
        if is_address(data):
            return type_str, to_canonical_address(data)
    return None


@implicitly_identity
def abi_address_to_bech32(type_str: TypeStr, data: Any) -> Optional[Tuple[TypeStr, Bech32Address]]:
    if type_str == 'address':
        validate_address(data)
        if is_address(data):
            return type_str, to_bech32_address(data)
    return None


@curry
def abi_ens_resolver(w3: "Web3", type_str: TypeStr, val: Any) -> Tuple[TypeStr, Any]:
    if type_str == 'address' and is_ens_name(val):
        if w3 is None:
            raise InvalidAddress(
                "Could not look up name %r because no platon"
                " connection available" % (val)
            )
        elif w3.ens is None:
            raise InvalidAddress(
                "Could not look up name %r because ENS is"
                " set to None" % (val)
            )
        elif int(w3.net.version) != 1 and not isinstance(w3.ens, StaticENS):
            raise InvalidAddress(
                "Could not look up name %r because platon is"
                " not connected to mainnet" % (val)
            )
        else:
            return type_str, validate_name_has_address(w3.ens, val)
    else:
        return type_str, val


BASE_RETURN_NORMALIZERS = [
    addresses_bech32,
]


if LooseVersion(platon_abi.__version__) < LooseVersion("2"):
    BASE_RETURN_NORMALIZERS.append(decode_abi_strings)


#
# Property Normalizers
#


def normalize_abi(abi: Union[ABI, str]) -> ABI:
    if isinstance(abi, str):
        abi = json.loads(abi)
    validate_abi(cast(ABI, abi))
    return cast(ABI, abi)


def normalize_address(ens: ENS, address: Bech32Address) -> Bech32Address:
    if address:
        if is_ens_name(address):
            validate_name_has_address(ens, address)
        else:
            validate_address(address)
    return address


def normalize_bytecode(bytecode: bytes) -> HexBytes:
    if bytecode:
        bytecode = HexBytes(bytecode)
    # type ignored b/c bytecode is converted to HexBytes above
    return bytecode  # type: ignore
