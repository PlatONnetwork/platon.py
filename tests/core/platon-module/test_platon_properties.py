import pytest


def test_platon_protocol_version(web3):
    assert web3.platon.protocol_version == '63'


def test_platon_protocolVersion(web3):
    with pytest.warns(DeprecationWarning):
        assert web3.platon.protocolVersion == '63'


def test_platon_chain_id(web3):
    assert web3.platon.chain_id == 61


def test_platon_chainId(web3):
    with pytest.warns(DeprecationWarning):
        assert web3.platon.chain_id == 61
