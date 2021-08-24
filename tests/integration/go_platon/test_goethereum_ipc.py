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


def _node_command_arguments(node_ipc_path,
                            base_node_command_arguments):

    node_port = get_open_port()
    yield from base_node_command_arguments
    yield from (
        '--port', node_port,
        '--ipcpath', node_ipc_path,
    )


@pytest.fixture(scope='module')
def node_command_arguments(node_ipc_path,
                           base_node_command_arguments):

    return _node_command_arguments(
        node_ipc_path,
        base_node_command_arguments
    )


@pytest.fixture(scope='module')
def node_ipc_path(datadir):
    node_ipc_dir_path = tempfile.mkdtemp()
    _node_ipc_path = os.path.join(node_ipc_dir_path, 'node.ipc')
    yield _node_ipc_path

    if os.path.exists(_node_ipc_path):
        os.remove(_node_ipc_path)


@pytest.fixture(scope="module")
def web3(node_process, node_ipc_path):
    wait_for_socket(node_ipc_path)
    _web3 = Web3(Web3.IPCProvider(node_ipc_path))
    return _web3


class TestGoPlatonTest(GoPlatonTest):
    pass


class TestGoPlatonAdminModuleTest(GoPlatonAdminModuleTest):
    @pytest.mark.xfail(reason="running node with the --nodiscover flag doesn't allow peer addition")
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
