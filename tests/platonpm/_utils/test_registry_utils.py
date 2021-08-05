import pytest

from platonpm.exceptions import (
    PlatonPMValidationError,
)
from platonpm.validation.uri import (
    validate_registry_uri,
)


@pytest.mark.parametrize(
    "uri",
    (
        # no package id in uri
        ("erc1319://zeppelinos.platon"),
        ("erc1319://zeppelinos.platon:1"),
        ("erc1319://zeppelinos.platon:1/"),
        ("erc1319://packages.zeppelinos.platon"),
        ("erc1319://packages.zeppelinos.platon:1"),
        ("erc1319://packages.zeppelinos.platon:1/"),
        ("erc1319://0xd3CdA913deB6f67967B99D67aCDFa1712C293601"),
        ("erc1319://0xd3CdA913deB6f67967B99D67aCDFa1712C293601:1"),
        ("erc1319://0xd3CdA913deB6f67967B99D67aCDFa1712C293601:1/"),
        # with package id in uri
        ("erc1319://zeppelinos.platon/erc20/"),
        ("erc1319://zeppelinos.platon:1/erc20/"),
        ("erc1319://zeppelinos.platon:1/erc20//"),
        ("erc1319://zeppelinos.platon/erc20@1.0.0"),
        ("erc1319://zeppelinos.platon:1/erc20@1.0.0"),
        ("erc1319://zeppelinos.platon:1/erc20@1.0.0/"),
        ("erc1319://packages.zeppelinos.platon/erc20@"),
        ("erc1319://packages.zeppelinos.platon:1/erc20@"),
        ("erc1319://packages.zeppelinos.platon:1/erc20@/"),
        ("erc1319://packages.zeppelinos.platon/erc20@1.0.0"),
        ("erc1319://packages.zeppelinos.platon:1/erc20@1.0.0"),
        ("erc1319://packages.zeppelinos.platon:1/erc20@1.0.0/"),
        ("erc1319://packages.platon.platon/greeter@%3E%3D1.0.2%2C%3C2"),
        ("erc1319://packages.platon.platon:1/greeter@%3E%3D1.0.2%2C%3C2"),
        ("erc1319://0xd3CdA913deB6f67967B99D67aCDFa1712C293601/erc20@1.0.0"),
        ("erc1319://0xd3CdA913deB6f67967B99D67aCDFa1712C293601:1/erc20@1.0.0"),
        ("erc1319://0xd3CdA913deB6f67967B99D67aCDFa1712C293601:1/erc20@1.0.0/"),
        ("erc1319://0xd3CdA913deB6f67967B99D67aCDFa1712C293601:1/erc20@1.0.0/deployments/ERC139")
    ),
)
def test_is_registry_uri_validates(uri):
    assert validate_registry_uri(uri) is None


@pytest.mark.parametrize(
    "uri",
    (
        # invalid authority
        ("erc1319://zeppelinos.platon:333/erc20@1.0.0"),
        ("erc1319://packages.zeppelinos.com:1/erc20@1.0.0"),
        ("erc1319://package.manager.zeppelinos.platon:1/erc20@1.0.0"),
        ("erc1319://packageszeppelinoseth:1/erc20@1.0.0"),
        ("erc1319://0xd3cda913deb6f67967b99d67acdfa1712c293601:1/erc20@1.0.0"),
        # invalid package name
        ("erc1319://packages.zeppelinos.platon/@1.0.0"),
        ("erc1319://packages.zeppelinos.platon:1/@1.0.0"),
        ("erc1319://packages.zeppelinos.platon:1/@1.0.0/"),
        ("erc1319://packages.zeppelinos.platon/!rc20?@1.0.0"),
        ("erc1319://packages.zeppelinos.platon:1/!rc20?@1.0.0"),
        ("erc1319://packages.zeppelinos.platon:1/!rc20?@1.0.0/"),
        # malformed
        ("erc1319packageszeppelinosetherc20@1.0.0"),
        ("erc1319:packages.zeppelinos.platon:1/erc20@1.0.0"),
        ("erc1319:packages.zeppelinos.platon:1/erc20@1.0.0/"),
        ("erc1319:/packages.zeppelinos.platon:1/erc20@1.0.0"),
        ("erc1319:/packages.zeppelinos.platon:1/erc20@1.0.0/"),
        ("erc1319/packages.zeppelinos.platon:1/erc20@1.0.0"),
        ("erc1319//packages.zeppelinos.platon:1/erc20@1.0.0"),
        ("erc1319packages.zeppelinos.platon:1/erc20@1.0.0"),
        # wrong scheme
        ("http://packages.zeppelinos.platon:1/erc20@1.0.0"),
        ("ercXX://packages.zeppelinos.platon:1/erc20@1.0.0"),
        # no path
        ("erc1319://"),
        ("1234"),
    ),
)
def test_is_registry_uri_raises_exception_for_invalid_uris(uri):
    with pytest.raises(PlatonPMValidationError):
        validate_registry_uri(uri)
