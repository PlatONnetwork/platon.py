import pytest

from platon import (
    PlatonTesterProvider,
    Web3,
)
from platon.platon import (
    Platon,
)
from platon.providers.platon_tester.main import (
    AsyncPlatonTesterProvider,
)
from platon.version import (
    AsyncVersion,
    Version,
    Version,
)

# This file is being left in since the Version module is being experimented on for
# async behavior. But, this file along with platon/version.py should be removed eventually.


@pytest.fixture
def blocking_w3():
    return Web3(
        PlatonTesterProvider(),
        modules={
            "blocking_version": (Version,),
            "legacy_version": (Version,),
            "platon": (Platon,),
        })


@pytest.fixture
def async_w3():
    return Web3(
        AsyncPlatonTesterProvider(),
        middlewares=[],
        modules={
            'async_version': (AsyncVersion,),
        })


def test_legacy_version_deprecation(blocking_w3):
    with pytest.raises(DeprecationWarning):
        blocking_w3.legacy_version.node
    with pytest.raises(DeprecationWarning):
        blocking_w3.legacy_version.platon


@pytest.mark.asyncio
async def test_async_blocking_version(async_w3, blocking_w3):
    assert async_w3.async_version.api == blocking_w3.api

    assert await async_w3.async_version.node == blocking_w3.clientVersion
    with pytest.warns(DeprecationWarning):
        assert await async_w3.async_version.platon == blocking_w3.platon.protocol_version
