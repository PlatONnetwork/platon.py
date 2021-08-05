import pytest
import random

from flaky import (
    flaky,
)

from platon._utils.threads import (
    Timeout,
)


@flaky(max_runs=3)
def test_miner_set_gas_price(web3_empty, wait_for_block):
    web3 = web3_empty

    initial_gas_price = web3.platon.gas_price

    # sanity check
    assert web3.platon.gas_price > 1000

    web3.gplaton.miner.set_gas_price(initial_gas_price // 2)

    with Timeout(60) as timeout:
        while web3.platon.gas_price == initial_gas_price:
            timeout.sleep(random.random())

    after_gas_price = web3.platon.gas_price
    assert after_gas_price < initial_gas_price


@flaky(max_runs=3)
def test_miner_setGasPrice(web3_empty, wait_for_block):
    web3 = web3_empty

    initial_gas_price = web3.platon.gas_price
    assert web3.platon.gas_price > 1000

    # sanity check

    with pytest.warns(DeprecationWarning):
        web3.gplaton.miner.setGasPrice(initial_gas_price // 2)

    with Timeout(60) as timeout:
        while web3.platon.gas_price == initial_gas_price:
            timeout.sleep(random.random())

    after_gas_price = web3.platon.gas_price
    assert after_gas_price < initial_gas_price
