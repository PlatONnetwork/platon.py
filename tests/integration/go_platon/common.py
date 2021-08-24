import pytest

from platon._utils.module_testing import (  # noqa: F401
    AsyncPlatonModuleTest,
    PlatonModuleTest,
    GoPlatonAdminModuleTest,
    GoPlatonPersonalModuleTest,
    NetModuleTest,
    VersionModuleTest,
    Web3ModuleTest,
)


class GoPlatonTest(Web3ModuleTest):
    def _check_web3_clientVersion(self, client_version):
        assert client_version.startswith('Node/')


class GoPlatonPlatonModuleTest(PlatonModuleTest):
    @pytest.mark.xfail(reason='platon_signTypedData has not been released in node')
    def test_platon_sign_typed_data(self, web3, unlocked_account_dual_type):
        super().test_platon_sign_typed_data(web3, unlocked_account_dual_type)

    @pytest.mark.xfail(reason='platon_signTypedData has not been released in node')
    def test_invalid_platon_sign_typed_data(self, web3, unlocked_account_dual_type):
        super().test_invalid_platon_sign_typed_data(web3, unlocked_account_dual_type)

    @pytest.mark.xfail(reason='platon_protocolVersion was removed in Node 1.10.0')
    def test_platon_protocol_version(self, web3):
        super().test_platon_protocol_version(web3)

    @pytest.mark.xfail(reason='platon_protocolVersion was removed in Node 1.10.0')
    def test_platon_protocolVersion(self, web3):
        super().test_platon_protocolVersion(web3)


class GoPlatonVersionModuleTest(VersionModuleTest):
    @pytest.mark.xfail(reason='platon_protocolVersion was removed in Node 1.10.0')
    def test_platon_protocol_version(self, web3):
        super().test_platon_protocol_version(web3)

    @pytest.mark.xfail(reason='platon_protocolVersion was removed in Node 1.10.0')
    def test_platon_protocolVersion(self, web3):
        super().test_platon_protocolVersion(web3)


class GoPlatonNetModuleTest(NetModuleTest):
    pass


class GoPlatonAdminModuleTest(GoPlatonAdminModuleTest):
    pass


class GoPlatonPersonalModuleTest(GoPlatonPersonalModuleTest):
    pass


class GoPlatonAsyncPlatonModuleTest(AsyncPlatonModuleTest):
    pass
