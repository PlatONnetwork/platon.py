from platon import Web3
from platon.providers.auto import (
    AutoProvider,
)
from platon.providers.platon_tester import (
    PlatonTesterProvider,
)


def test_set_provider(web3):
    provider = PlatonTesterProvider()

    web3.provider = provider

    assert web3.provider == provider


def test_auto_provider_none():
    # init without provider succeeds, even when no provider available
    w3 = Web3()

    # non-node requests succeed
    w3.toHex(0) == '0x0'

    type(w3.provider) == AutoProvider
