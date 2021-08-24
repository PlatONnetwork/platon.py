import random

from flaky import (
    flaky,
)

from platon._utils.threads import (
    Timeout,
)


@flaky(max_runs=3)
def test_miner_start(web3_empty, wait_for_miner_start):
    web3 = web3_empty

    # sanity
    assert web3.platon.mining
    assert web3.platon.hashrate

    web3.node.miner.stop()

    with Timeout(60) as timeout:
        while web3.platon.mining or web3.platon.hashrate:
            timeout.sleep(random.random())

    assert not web3.platon.mining
    assert not web3.platon.hashrate

    web3.miner.start(1)

    wait_for_miner_start(web3)

    assert web3.platon.mining
    assert web3.platon.hashrate
