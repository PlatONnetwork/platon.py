from platon._utils.threads import (
    Timeout,
)
from platon.providers.platon_tester import (
    PlatonTesterProvider,
)


def test_sync_filter_against_latest_blocks(web3, sleep_interval, wait_for_block):
    if not isinstance(web3.provider, PlatonTesterProvider):
        web3.provider = PlatonTesterProvider()

    txn_filter = web3.platon.filter("latest")

    current_block = web3.platon.block_number

    wait_for_block(web3, current_block + 3)

    found_block_hashes = []
    with Timeout(5) as timeout:
        while len(found_block_hashes) < 3:
            found_block_hashes.extend(txn_filter.get_new_entries())
            timeout.sleep(sleep_interval())

    assert len(found_block_hashes) == 3

    expected_block_hashes = [
        web3.platon.get_block(n + 1).hash for n in range(current_block, current_block + 3)
    ]
    assert found_block_hashes == expected_block_hashes
