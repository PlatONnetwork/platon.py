import pytest

from platon._utils.threads import (
    Timeout,
)
from platon.providers.platon_tester import (
    PlatonTesterProvider,
)


@pytest.fixture()
def filter_id(web3):
    if not isinstance(web3.provider, PlatonTesterProvider):
        web3.provider = PlatonTesterProvider()

    block_filter = web3.platon.filter("latest")
    return block_filter.filter_id


def test_instantiate_existing_filter(web3, sleep_interval, wait_for_block, filter_id):
    with pytest.raises(TypeError):
        web3.platon.filter('latest', filter_id)
    with pytest.raises(TypeError):
        web3.platon.filter('latest', filter_id=filter_id)
    with pytest.raises(TypeError):
        web3.platon.filter(filter_params='latest', filter_id=filter_id)

    block_filter = web3.platon.filter(filter_id=filter_id)

    current_block = web3.platon.block_number

    wait_for_block(web3, current_block + 3)

    found_block_hashes = []
    with Timeout(5) as timeout:
        while len(found_block_hashes) < 3:
            found_block_hashes.extend(block_filter.get_new_entries())
            timeout.sleep(sleep_interval())

    assert len(found_block_hashes) == 3

    expected_block_hashes = [
        web3.platon.get_block(n + 1).hash for n in range(current_block, current_block + 3)
    ]
    assert found_block_hashes == expected_block_hashes
