import os
import pytest
import tempfile

from tests.utils import (
    get_open_port,
)
from platon import Web3

from .common import (
    GoPlatonAdminModuleTest,
    GoPlatonPlatonModuleTest,
    GoPlatonNetModuleTest,
    GoPlatonPersonalModuleTest,
    GoPlatonTest,
    GoPlatonVersionModuleTest,
)
from .utils import (
    wait_for_socket,
)


def _gplaton_command_arguments(gplaton_ipc_path,
                            base_gplaton_command_arguments):

    gplaton_port = get_open_port()
    yield from base_gplaton_command_arguments
    yield from (
        '--port', gplaton_port,
        '--ipcpath', gplaton_ipc_path,
    )


@pytest.fixture(scope='module')
def gplaton_command_arguments(gplaton_ipc_path,
                           base_gplaton_command_arguments):

    return _gplaton_command_arguments(
        gplaton_ipc_path,
        base_gplaton_command_arguments
    )


@pytest.fixture(scope='module')
def gplaton_ipc_path(datadir):
    gplaton_ipc_dir_path = tempfile.mkdtemp()
    _gplaton_ipc_path = os.path.join(gplaton_ipc_dir_path, 'gplaton.ipc')
    yield _gplaton_ipc_path

    if os.path.exists(_gplaton_ipc_path):
        os.remove(_gplaton_ipc_path)


@pytest.fixture(scope="module")
def web3(gplaton_process, gplaton_ipc_path):
    wait_for_socket(gplaton_ipc_path)
    _web3 = Web3(Web3.IPCProvider(gplaton_ipc_path))
    return _web3


class TestGoPlatonTest(GoPlatonTest):
    pass


class TestGoPlatonAdminModuleTest(GoPlatonAdminModuleTest):
    @pytest.mark.xfail(reason="running gplaton with the --nodiscover flag doesn't allow peer addition")
    def test_admin_peers(web3):
        super().test_admin_peers(web3)

    @pytest.mark.xfail(reason="websockets aren't enabled with our IPC flags")
    def test_admin_start_stop_ws(web3):
        super().test_admin_start_stop_ws(web3)


class TestGoPlatonPlatonModuleTest(GoPlatonPlatonModuleTest):
    pass


class TestGoPlatonVersionModuleTest(GoPlatonVersionModuleTest):
    pass


class TestGoPlatonNetModuleTest(GoPlatonNetModuleTest):
    pass


class TestGoPlatonPersonalModuleTest(GoPlatonPersonalModuleTest):
    pass
