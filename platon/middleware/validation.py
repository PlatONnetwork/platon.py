from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
)

from platon_utils.curried import (
    apply_formatter_at_index,
    apply_formatter_if,
    apply_formatters_to_dict,
    is_null,
    is_string,
)
from platon_utils.toolz import (
    complement,
    compose,
    curry,
    dissoc,
)
from hexbytes import (
    HexBytes,
)

from platon._utils.formatters import (
    hex_to_integer,
)
from platon._utils.rpc_abi import (
    RPC,
)
from platon.exceptions import (
    ExtraDataLengthError,
    ValidationError,
)
from platon.middleware.formatting import (
    construct_web3_formatting_middleware,
)
from platon.types import (
    FormattersDict,
    TxParams,
)

if TYPE_CHECKING:
    from platon import Web3

MAX_EXTRADATA_LENGTH = 328

is_not_null = complement(is_null)

to_integer_if_hex = apply_formatter_if(is_string, hex_to_integer)


@curry
def validate_chain_id(web3: "Web3", chain_id: int) -> int:
    if to_integer_if_hex(chain_id) == web3.platon.chain_id:
        return chain_id
    else:
        raise ValidationError(
            "The transaction declared chain ID %r, "
            "but the connected node is on %r" % (
                chain_id,
                web3.platon.chain_id,
            )
        )


def check_extradata_length(val: Any) -> Any:
    if not isinstance(val, (str, int, bytes)):
        return val
    result = HexBytes(val)
    if len(result) > MAX_EXTRADATA_LENGTH:
        raise ExtraDataLengthError(
            "The field extraData is %d bytes, but should be %d. "
            "It is quite likely that you are connected to a POA chain. "
            "Refer to "
            "http://web3py.readthedocs.io/en/stable/middleware.html#node-style-proof-of-authority "
            "for more details. The full extraData is: %r" % (
                len(result), MAX_EXTRADATA_LENGTH, result
            )
        )
    return val


def transaction_normalizer(transaction: TxParams) -> TxParams:
    return dissoc(transaction, 'chainId')


def transaction_param_validator(web3: "Web3") -> Callable[..., Any]:
    transactions_params_validators = {
        "chain_id": apply_formatter_if(
            # Bypass `validate_chain_id` if chain_id can't be determined
            lambda _: is_not_null(web3.platon.chain_id),
            validate_chain_id(web3),
        ),
    }
    return apply_formatter_at_index(
        apply_formatters_to_dict(transactions_params_validators),
        0
    )


BLOCK_VALIDATORS = {
    'extraData': check_extradata_length,
}


block_validator = apply_formatter_if(
    is_not_null,
    apply_formatters_to_dict(BLOCK_VALIDATORS)
)


@curry
def chain_id_validator(web3: "Web3") -> Callable[..., Any]:
    return compose(
        apply_formatter_at_index(transaction_normalizer, 0),
        transaction_param_validator(web3)
    )


def build_validators_with_web3(w3: "Web3") -> FormattersDict:
    return dict(
        request_formatters={
            RPC.platon_sendTransaction: chain_id_validator(w3),
            RPC.platon_estimateGas: chain_id_validator(w3),
            RPC.platon_call: chain_id_validator(w3),
        },
        result_formatters={
            RPC.platon_getBlockByHash: block_validator,
            RPC.platon_getBlockByNumber: block_validator,
        },
    )


validation_middleware = construct_web3_formatting_middleware(build_validators_with_web3)
