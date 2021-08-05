import pytest

from tests.utils import (
    get_open_port,
)
from platon import Web3
from platon.platon import (
    AsyncPlaton,
)
from platon.middleware import (
    async_buffered_gas_estimate_middleware,
    async_gas_price_strategy_middleware,
)
from platon.providers.async_rpc import (
    AsyncHTTPProvider,
)

from .common import (
    GoPlatonAdminModuleTest,
    GoPlatonAsyncPlatonModuleTest,
    GoPlatonPlatonModuleTest,
    GoPlatonNetModuleTest,
    GoPlatonPersonalModuleTest,
    GoPlatonTest,
    GoPlatonVersionModuleTest,
)
from .utils import (
    wait_for_aiohttp,
    wait_for_http,
)


@pytest.fixture(scope="module")
def rpc_port():
    return get_open_port()


@pytest.fixture(scope="module")
def endpoint_uri(rpc_port):
    return 'http://localhost:{0}'.format(rpc_port)


def _gplaton_command_arguments(rpc_port,
                            base_gplaton_command_arguments,
                            gplaton_version):
    yield from base_gplaton_command_arguments
    if gplaton_version.major == 1:
        yield from (
            '--http',
            '--http.port', rpc_port,
            '--http.api', 'admin,platon,net,platon,personal,miner',
            '--ipcdisable',
            '--allow-insecure-unlock'
        )
    else:
        raise AssertionError("Unsupported Gplaton version")


@pytest.fixture(scope='module')
def gplaton_command_arguments(rpc_port,
                           base_gplaton_command_arguments,
                           get_gplaton_version):

    return _gplaton_command_arguments(
        rpc_port,
        base_gplaton_command_arguments,
        get_gplaton_version
    )


@pytest.fixture(scope="module")
def web3(gplaton_process, endpoint_uri):
    wait_for_http(endpoint_uri)
    _web3 = Web3(Web3.HTTPProvider(endpoint_uri))
    return _web3


@pytest.fixture(scope="module")
async def async_w3(gplaton_process, endpoint_uri):
    await wait_for_aiohttp(endpoint_uri)
    _web3 = Web3(
        AsyncHTTPProvider(endpoint_uri),
        middlewares=[
            async_gas_price_strategy_middleware,
            async_buffered_gas_estimate_middleware
        ],
        modules={'platon': (AsyncPlaton,)})
    return _web3


class TestGoPlatonTest(GoPlatonTest):
    pass


class TestGoPlatonAdminModuleTest(GoPlatonAdminModuleTest):
    @pytest.mark.xfail(reason="running gplaton with the --nodiscover flag doesn't allow peer addition")
    def test_admin_peers(self, web3: "Web3") -> None:
        super().test_admin_peers(web3)

    def test_admin_start_stop_rpc(self, web3: "Web3") -> None:
        # This test causes all tests after it to fail on CI if it's allowed to run
        pytest.xfail(reason='Only one RPC endpoint is allowed to be active at any time')
        super().test_admin_start_stop_rpc(web3)

    def test_admin_start_stop_ws(self, web3: "Web3") -> None:
        # This test causes all tests after it to fail on CI if it's allowed to run
        pytest.xfail(reason='Only one WS endpoint is allowed to be active at any time')
        super().test_admin_start_stop_ws(web3)


class TestGoPlatonPlatonModuleTest(GoPlatonPlatonModuleTest):
    pass


class TestGoPlatonVersionModuleTest(GoPlatonVersionModuleTest):
    pass


class TestGoPlatonNetModuleTest(GoPlatonNetModuleTest):
    pass


class TestGoPlatonPersonalModuleTest(GoPlatonPersonalModuleTest):
    pass


class TestGoPlatonAsyncPlatonModuleTest(GoPlatonAsyncPlatonModuleTest):
    pass
