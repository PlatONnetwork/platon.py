import functools
import pytest

from platon_tester import (
    PlatonTester,
)
from platon_tester.exceptions import (
    TransactionFailed,
)
from platon_utils import (
    is_bech32_address,
    is_dict,
    is_integer,
)

from platon import Web3
from platon._utils.module_testing import (
    PlatonModuleTest,
    GoPlatonPersonalModuleTest,
    NetModuleTest,
    VersionModuleTest,
    Web3ModuleTest,
)
from platon._utils.module_testing.emitter_contract import (
    EMITTER_ENUM,
)
from platon.providers.platon_tester import (
    PlatonTesterProvider,
)
from platon.types import (
    BlockData,
)


@pytest.fixture(scope="module")
def platon_tester():
    _platon_tester = PlatonTester()
    return _platon_tester


@pytest.fixture(scope="module")
def platon_tester_provider(platon_tester):
    provider = PlatonTesterProvider(platon_tester)
    return provider


@pytest.fixture(scope="module")
def web3(platon_tester_provider):
    _web3 = Web3(platon_tester_provider)
    return _web3


#
# Math Contract Setup
#
@pytest.fixture(scope="module")
def math_contract_deploy_txn_hash(web3, math_contract_factory):
    deploy_txn_hash = math_contract_factory.constructor().transact({'from': web3.platon.coinbase})
    return deploy_txn_hash


@pytest.fixture(scope="module")
def math_contract(web3, math_contract_factory, math_contract_deploy_txn_hash):
    deploy_receipt = web3.platon.wait_for_transaction_receipt(math_contract_deploy_txn_hash)
    assert is_dict(deploy_receipt)
    contract_address = deploy_receipt['contractAddress']
    assert is_bech32_address(contract_address)
    return math_contract_factory(contract_address)


@pytest.fixture(scope="module")
def math_contract_address(math_contract, address_conversion_func):
    return address_conversion_func(math_contract.address)

#
# Emitter Contract Setup
#


@pytest.fixture(scope="module")
def emitter_contract_deploy_txn_hash(web3, emitter_contract_factory):
    deploy_txn_hash = emitter_contract_factory.constructor().transact({'from': web3.platon.coinbase})
    return deploy_txn_hash


@pytest.fixture(scope="module")
def emitter_contract(web3, emitter_contract_factory, emitter_contract_deploy_txn_hash):
    deploy_receipt = web3.platon.wait_for_transaction_receipt(emitter_contract_deploy_txn_hash)
    assert is_dict(deploy_receipt)
    contract_address = deploy_receipt['contractAddress']
    assert is_bech32_address(contract_address)
    return emitter_contract_factory(contract_address)


@pytest.fixture(scope="module")
def emitter_contract_address(emitter_contract, address_conversion_func):
    return address_conversion_func(emitter_contract.address)


@pytest.fixture(scope="module")
def empty_block(web3):
    web3.testing.mine()
    block = web3.platon.get_block("latest")
    assert not block['transactions']
    return block


@pytest.fixture(scope="module")
def block_with_txn(web3):
    txn_hash = web3.platon.send_transaction({
        'from': web3.platon.coinbase,
        'to': web3.platon.coinbase,
        'value': 1,
        'gas': 21000,
        'gas_price': 1,
    })
    txn = web3.platon.get_transaction(txn_hash)
    block = web3.platon.get_block(txn['blockNumber'])
    return block


@pytest.fixture(scope="module")
def mined_txn_hash(block_with_txn):
    return block_with_txn['transactions'][0]


@pytest.fixture(scope="module")
def block_with_txn_with_log(web3, emitter_contract):
    txn_hash = emitter_contract.functions.logDouble(
        which=EMITTER_ENUM['LogDoubleWithIndex'], arg0=12345, arg1=54321,
    ).transact({
        'from': web3.platon.coinbase,
    })
    txn = web3.platon.get_transaction(txn_hash)
    block = web3.platon.get_block(txn['blockNumber'])
    return block


@pytest.fixture(scope="module")
def txn_hash_with_log(block_with_txn_with_log):
    return block_with_txn_with_log['transactions'][0]


#
# Revert Contract Setup
#
@pytest.fixture(scope="module")
def revert_contract_deploy_txn_hash(web3, revert_contract_factory):
    deploy_txn_hash = revert_contract_factory.constructor().transact({'from': web3.platon.coinbase})
    return deploy_txn_hash


@pytest.fixture(scope="module")
def revert_contract(web3, revert_contract_factory, revert_contract_deploy_txn_hash):
    deploy_receipt = web3.platon.wait_for_transaction_receipt(revert_contract_deploy_txn_hash)
    assert is_dict(deploy_receipt)
    contract_address = deploy_receipt['contractAddress']
    assert is_bech32_address(contract_address)
    return revert_contract_factory(contract_address)


UNLOCKABLE_PRIVATE_KEY = '0x392f63a79b1ff8774845f3fa69de4a13800a59e7083f5187f1558f0797ad0f01'


@pytest.fixture(scope='module')
def unlockable_account_pw(web3):
    return 'platon-testing'


@pytest.fixture(scope='module')
def unlockable_account(web3, unlockable_account_pw):
    account = web3.node.personal.import_raw_key(UNLOCKABLE_PRIVATE_KEY, unlockable_account_pw)
    web3.platon.send_transaction({
        'from': web3.platon.coinbase,
        'to': account,
        'value': web3.toVon(10, 'ether'),
    })
    yield account


@pytest.fixture
def unlocked_account(web3, unlockable_account, unlockable_account_pw):
    web3.node.personal.unlock_account(unlockable_account, unlockable_account_pw)
    yield unlockable_account
    web3.node.personal.lock_account(unlockable_account)


@pytest.fixture()
def unlockable_account_dual_type(unlockable_account, address_conversion_func):
    return address_conversion_func(unlockable_account)


@pytest.fixture
def unlocked_account_dual_type(web3, unlockable_account_dual_type, unlockable_account_pw):
    web3.node.personal.unlock_account(unlockable_account_dual_type, unlockable_account_pw)
    yield unlockable_account_dual_type
    web3.node.personal.lock_account(unlockable_account_dual_type)


@pytest.fixture(scope="module")
def funded_account_for_raw_txn(web3):
    account = '0x39EEed73fb1D3855E90Cbd42f348b3D7b340aAA6'
    web3.platon.send_transaction({
        'from': web3.platon.coinbase,
        'to': account,
        'value': web3.toVon(10, 'ether'),
        'gas': 21000,
        'gas_price': 1,
    })
    return account


class TestPlatonTesterWeb3Module(Web3ModuleTest):
    def _check_web3_clientVersion(self, client_version):
        assert client_version.startswith('PlatonTester/')


def not_implemented(method, exc_type=NotImplementedError):
    @functools.wraps(method)
    def inner(*args, **kwargs):
        with pytest.raises(exc_type):
            method(*args, **kwargs)
    return inner


def disable_auto_mine(func):
    @functools.wraps(func)
    def func_wrapper(self, platon_tester, *args, **kwargs):
        snapshot = platon_tester.take_snapshot()
        platon_tester.disable_auto_mine_transactions()
        try:
            func(self, platon_tester, *args, **kwargs)
        finally:
            platon_tester.enable_auto_mine_transactions()
            platon_tester.mine_block()
            platon_tester.revert_to_snapshot(snapshot)
    return func_wrapper


class TestPlatonTesterPlatonModule(PlatonModuleTest):
    test_platon_sign = not_implemented(PlatonModuleTest.test_platon_sign, ValueError)
    test_platon_sign_ens_names = not_implemented(
        PlatonModuleTest.test_platon_sign_ens_names, ValueError
    )
    test_platon_sign_typed_data = not_implemented(
        PlatonModuleTest.test_platon_sign_typed_data,
        ValueError
    )
    test_platon_sign_transaction = not_implemented(PlatonModuleTest.test_platon_sign_transaction, ValueError)
    test_platon_sign_transaction_ens_names = not_implemented(
        PlatonModuleTest.test_platon_sign_transaction_ens_names, ValueError
    )
    test_platon_submit_hashrate = not_implemented(PlatonModuleTest.test_platon_submit_hashrate, ValueError)
    test_platon_submit_work = not_implemented(PlatonModuleTest.test_platon_submit_work, ValueError)

    def test_platon_getBlockByHash_pending(
        self, web3: "Web3"
    ) -> None:
        block = web3.platon.get_block('pending')
        assert block['hash'] is not None

    @pytest.mark.xfail(reason='EIP 1559 is not implemented on platon-tester')
    def test_platon_get_transaction_receipt_unmined(self, platon_tester, web3, unlocked_account):
        super().test_platon_get_transaction_receipt_unmined(web3, unlocked_account)

    @disable_auto_mine
    def test_platon_replace_transaction_legacy(self, platon_tester, web3, unlocked_account):
        super().test_platon_replace_transaction_legacy(web3, unlocked_account)

    @pytest.mark.xfail(reason='EIP 1559 is not implemented on platon-tester')
    def test_platon_replace_transaction(self, platon_tester, web3, unlocked_account):
        super().test_platon_replace_transaction(web3, unlocked_account)

    @pytest.mark.xfail(reason='EIP 1559 is not implemented on platon-tester')
    def test_platon_replace_transaction_underpriced(self, web3, emitter_contract_address):
        super().test_platon_replace_transaction_underpriced(web3, emitter_contract_address)

    @pytest.mark.xfail(reason='EIP 1559 is not implemented on platon-tester')
    def test_platon_replace_transaction_already_mined(self, web3, emitter_contract_address):
        super().test_platon_replace_transaction_already_mined(web3, emitter_contract_address)

    @pytest.mark.xfail(reason='EIP 1559 is not implemented on platon-tester')
    def test_platon_replace_transaction_incorrect_nonce(self, platon_tester, web3, unlocked_account):
        super().test_platon_replace_transaction_incorrect_nonce(web3, unlocked_account)

    @disable_auto_mine
    def test_platon_replace_transaction_gas_price_too_low(self, platon_tester, web3, unlocked_account):
        super().test_platon_replace_transaction_gas_price_too_low(web3, unlocked_account)

    @disable_auto_mine
    def test_platon_replace_transaction_gas_price_defaulting_minimum(self,
                                                                  platon_tester,
                                                                  web3,
                                                                  unlocked_account):
        super().test_platon_replace_transaction_gas_price_defaulting_minimum(web3, unlocked_account)

    @disable_auto_mine
    def test_platon_replace_transaction_gas_price_defaulting_strategy_higher(self,
                                                                          platon_tester,
                                                                          web3,
                                                                          unlocked_account):
        super().test_platon_replace_transaction_gas_price_defaulting_strategy_higher(
            web3, unlocked_account
        )

    @disable_auto_mine
    def test_platon_replace_transaction_gas_price_defaulting_strategy_lower(self,
                                                                         platon_tester,
                                                                         web3,
                                                                         unlocked_account):
        super().test_platon_replace_transaction_gas_price_defaulting_strategy_lower(
            web3, unlocked_account
        )

    @disable_auto_mine
    def test_platon_modify_transaction_legacy(self, platon_tester, web3, unlocked_account):
        super().test_platon_modify_transaction_legacy(web3, unlocked_account)

    @pytest.mark.xfail(reason='EIP 1559 is not implemented on platon-tester')
    def test_platon_modify_transaction(self, platon_tester, web3, unlocked_account):
        super().test_platon_modify_transaction(web3, unlocked_account)

    @disable_auto_mine
    def test_platon_call_old_contract_state(self, platon_tester, web3, math_contract, unlocked_account):
        # For now, platon tester cannot give call results in the pending block.
        # Once that feature is added, then delete the except/else blocks.
        try:
            super().test_platon_call_old_contract_state(web3, math_contract, unlocked_account)
        except AssertionError as err:
            if str(err) == "pending call result was 0 instead of 1":
                pass
            else:
                raise err
        else:
            raise AssertionError("platon-tester was unexpectedly able to give the pending call result")

    @pytest.mark.xfail(reason='json-rpc method is not implemented on platon-tester')
    def test_platon_get_storage_at(self, web3, emitter_contract_address):
        super().test_platon_get_storage_at(web3, emitter_contract_address)

    @pytest.mark.xfail(reason='json-rpc method is not implemented on platon-tester')
    def test_platon_get_storage_at_ens_name(self, web3, emitter_contract_address):
        super().test_platon_get_storage_at_ens_name(web3, emitter_contract_address)

    def test_platon_estimate_gas_with_block(self,
                                         web3,
                                         unlocked_account_dual_type):
        super().test_platon_estimate_gas_with_block(
            web3, unlocked_account_dual_type
        )

    def test_platon_chain_id(self, web3):
        chain_id = web3.platon.chain_id
        assert is_integer(chain_id)
        assert chain_id == 61

    def test_platon_chainId(self, web3):
        with pytest.warns(DeprecationWarning):
            chain_id = web3.platon.chain_id
        assert is_integer(chain_id)
        assert chain_id == 61

    @pytest.mark.xfail(raises=KeyError, reason="platon tester doesn't return 'to' key")
    def test_platon_get_transaction_receipt_mined(self, web3, block_with_txn, mined_txn_hash):
        super().test_platon_get_transaction_receipt_mined(web3, block_with_txn, mined_txn_hash)

    @pytest.mark.xfail(raises=TypeError, reason="call override param not implemented on platon-tester")
    def test_platon_call_with_override(self, web3, revert_contract):
        super().test_platon_call_with_override(web3, revert_contract)

    def test_platon_call_revert_with_msg(self, web3, revert_contract, unlocked_account):
        with pytest.raises(TransactionFailed,
                           match='execution reverted: Function has been reverted'):
            txn_params = revert_contract._prepare_transaction(
                fn_name="revertWithMessage",
                transaction={
                    "from": unlocked_account,
                    "to": revert_contract.address,
                },
            )
            web3.platon.call(txn_params)

    def test_platon_call_revert_without_msg(self, web3, revert_contract, unlocked_account):
        with pytest.raises(TransactionFailed, match="execution reverted"):
            txn_params = revert_contract._prepare_transaction(
                fn_name="revertWithoutMessage",
                transaction={
                    "from": unlocked_account,
                    "to": revert_contract.address,
                },
            )
            web3.platon.call(txn_params)

    def test_platon_estimate_gas_revert_with_msg(self, web3, revert_contract, unlocked_account):
        with pytest.raises(TransactionFailed,
                           match='execution reverted: Function has been reverted'):
            txn_params = revert_contract._prepare_transaction(
                fn_name="revertWithMessage",
                transaction={
                    "from": unlocked_account,
                    "to": revert_contract.address,
                },
            )
            web3.platon.estimate_gas(txn_params)

    def test_platon_estimate_gas_revert_without_msg(self, web3, revert_contract, unlocked_account):
        with pytest.raises(TransactionFailed, match="execution reverted"):
            txn_params = revert_contract._prepare_transaction(
                fn_name="revertWithoutMessage",
                transaction={
                    "from": unlocked_account,
                    "to": revert_contract.address,
                },
            )
            web3.platon.estimate_gas(txn_params)

    @pytest.mark.xfail(reason='EIP 1559 is not implemented on platon-tester')
    def test_platon_send_transaction(self, web3, emitter_contract_address):
        super().test_platon_send_transaction(web3, emitter_contract_address)

    @pytest.mark.xfail(reason='EIP 1559 is not implemented on platon-tester')
    def test_platon_send_transaction_with_nonce(self, web3, emitter_contract_address):
        super().test_platon_send_transaction_with_nonce(web3, emitter_contract_address)

    @pytest.mark.xfail(reason='EIP 1559 is not implemented on platon-tester')
    def test_platon_send_transaction_default_fees(self, web3, emitter_contract_address):
        super().test_platon_send_transaction_default_fees(web3, emitter_contract_address)

    @pytest.mark.xfail(reason='EIP 1559 is not implemented on platon-tester')
    def test_platon_send_transaction_hex_fees(self, web3, emitter_contract_address):
        super().test_platon_send_transaction_hex_fees(web3, emitter_contract_address)

    @pytest.mark.xfail(reason='EIP 1559 is not implemented on platon-tester')
    def test_platon_send_transaction_no_gas(self, web3, emitter_contract_address):
        super().test_platon_send_transaction_no_gas(web3, emitter_contract_address)

    @pytest.mark.xfail(reason='EIP 1559 is not implemented on platon-tester')
    def test_platon_send_transaction_no_max_fee(self, web3, emitter_contract_address):
        super().test_platon_send_transaction_no_max_fee(web3, emitter_contract_address)


class TestPlatonTesterVersionModule(VersionModuleTest):
    pass


class TestPlatonTesterNetModule(NetModuleTest):
    pass


# Use platon.node.personal namespace for testing platon-tester
class TestPlatonTesterPersonalModule(GoPlatonPersonalModuleTest):
    test_personal_sign_and_ecrecover = not_implemented(
        GoPlatonPersonalModuleTest.test_personal_sign_and_ecrecover,
        ValueError,
    )

    # Test overridden here since platon-tester returns False rather than None for failed unlock
    def test_personal_unlock_account_failure(self,
                                             web3,
                                             unlockable_account_dual_type):
        result = web3.node.personal.unlock_account(unlockable_account_dual_type, 'bad-password')
        assert result is False

    @pytest.mark.xfail(raises=ValueError, reason="list_wallets not implemented in platon-tester")
    def test_personal_list_wallets(self, web3: "Web3") -> None:
        super().test_personal_list_wallets(web3)
