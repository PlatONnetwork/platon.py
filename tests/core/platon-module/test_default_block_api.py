import pytest


@pytest.fixture(autouse=True)
def wait_for_first_block(web3, wait_for_block):
    wait_for_block(web3)


def test_uses_default_block(web3, extra_accounts,
                            wait_for_transaction):
    assert(web3.platon.default_block == 'latest')
    web3.platon.default_block = web3.platon.block_number
    assert(web3.platon.default_block == web3.platon.block_number)


def test_uses_defaultBlock_with_warning(web3, extra_accounts,
                                        wait_for_transaction):
    with pytest.warns(DeprecationWarning):
        assert web3.platon.defaultBlock == 'latest'

    with pytest.warns(DeprecationWarning):
        web3.platon.defaultBlock = web3.platon.block_number

    with pytest.warns(DeprecationWarning):
        assert(web3.platon.defaultBlock == web3.platon.block_number)
