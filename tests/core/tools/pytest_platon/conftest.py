from pathlib import (
    Path,
)
import pytest

from platonpm import (
    get_platonpm_spec_dir,
)
from platon import Web3

PYTEST_PLATON_TESTS_DIR = Path(__file__).parent


@pytest.fixture
def pte_assets_dir():
    return PYTEST_PLATON_TESTS_DIR / "assets"


@pytest.fixture
def w3():
    return Web3(Web3.PlatonTesterProvider())


@pytest.fixture
def platonpm_spec_dir():
    return get_platonpm_spec_dir()


@pytest.fixture
def escrow_deployer(deployer, platonpm_spec_dir):
    escrow_manifest_path = platonpm_spec_dir / "examples" / "escrow" / "v3.json"
    return deployer(escrow_manifest_path)
