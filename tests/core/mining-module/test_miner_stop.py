import random

from flaky import (
    flaky,
)

from platon._utils.threads import (
    Timeout,
)


@flaky(max_runs=3)
def test_miner_stop(web3_empty):
    web3 = web3_empty

    assert web3.platon.mining
    assert web3.platon.hashrate

    web3.node.miner.stop()

    with Timeout(60) as timeout:
        while web3.platon.mining or web3.platon.hashrate:
            timeout.sleep(random.random())
            timeout.check()

    assert not web3.platon.mining
    assert not web3.platon.hashrate
