import pytest


def test_miner_set_etherbase(web3_empty):
    web3 = web3_empty
    assert web3.platon.coinbase == web3.platon.accounts[0]
    new_account = web3.personal.newAccount('this-is-a-password')
    web3.gplaton.miner.set_etherbase(new_account)
    assert web3.platon.coinbase == new_account


def test_miner_setEtherbase(web3_empty):
    web3 = web3_empty
    assert web3.platon.coinbase == web3.platon.accounts[0]
    new_account = web3.personal.newAccount('this-is-a-password')
    with pytest.warns(DeprecationWarning):
        web3.gplaton.miner.setEtherbase(new_account)
    assert web3.platon.coinbase == new_account
