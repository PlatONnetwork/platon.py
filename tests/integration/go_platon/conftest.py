import json
import os
from pathlib import (
    Path,
)
import pytest
import subprocess
import zipfile

from platon_utils import (
    is_bech32_address,
    is_dict,
    to_text,
)

from .utils import (
    kill_proc_gracefully,
)

KEYFILE_PW = 'web3py-test'

NODE_FIXTURE_ZIP = 'node-1.10.4-fixture.zip'


@pytest.fixture(scope='module')
def node_binary():
    from node.install import (
        get_executable_path,
        install_node,
    )

    if 'NODE_BINARY' in os.environ:
        return os.environ['NODE_BINARY']
    elif 'NODE_VERSION' in os.environ:
        node_version = os.environ['NODE_VERSION']
        _node_binary = get_executable_path(node_version)
        if not os.path.exists(_node_binary):
            install_node(node_version)
        assert os.path.exists(_node_binary)
        return _node_binary
    else:
        return 'node'


def absolute_datadir(directory_name):
    return os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        '..',
        directory_name,
    ))


@pytest.fixture(scope="module")
def get_node_version(node_binary):
    from node import get_node_version
    return get_node_version(node_executable=os.path.expanduser(node_binary))


@pytest.fixture(scope="module")
def base_node_command_arguments(node_binary, datadir):
    return (
        node_binary,
        '--data_dir', str(datadir),
        '--nodiscover',
        '--fakepow',
    )


@pytest.fixture(scope="module")
def node_zipfile_version(get_node_version):
    if get_node_version.major == 1 and get_node_version.minor == 10:
        return NODE_FIXTURE_ZIP
    raise AssertionError("Unsupported node version")


@pytest.fixture(scope='module')
def datadir(tmpdir_factory, node_zipfile_version):
    zipfile_path = absolute_datadir(node_zipfile_version)
    base_dir = tmpdir_factory.mktemp('platon')
    tmp_datadir = os.path.join(str(base_dir), 'data_dir')
    with zipfile.ZipFile(zipfile_path, 'r') as zip_ref:
        zip_ref.extractall(tmp_datadir)
    return tmp_datadir


@pytest.fixture(scope="module")
def node_fixture_data(datadir):
    config_file_path = Path(datadir) / 'config.json'
    return json.loads(config_file_path.read_text())


@pytest.fixture(scope='module')
def genesis_file(datadir):
    genesis_file_path = os.path.join(datadir, 'genesis.json')
    return genesis_file_path


@pytest.fixture(scope='module')
def node_process(node_binary, datadir, genesis_file, node_command_arguments):
    init_datadir_command = (
        node_binary,
        '--data_dir', str(datadir),
        'init',
        str(genesis_file),
    )
    subprocess.check_output(
        init_datadir_command,
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    proc = subprocess.Popen(
        node_command_arguments,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        yield proc
    finally:
        kill_proc_gracefully(proc)
        output, errors = proc.communicate()
        print(
            "Node Process Exited:\n"
            "stdout:{0}\n\n"
            "stderr:{1}\n\n".format(
                to_text(output),
                to_text(errors),
            )
        )


@pytest.fixture(scope='module')
def coinbase(web3):
    return web3.platon.coinbase


@pytest.fixture(scope="module")
def math_contract_deploy_txn_hash(node_fixture_data):
    return node_fixture_data['math_deploy_txn_hash']


@pytest.fixture(scope="module")
def math_contract(web3, math_contract_factory, node_fixture_data):
    return math_contract_factory(address=node_fixture_data['math_address'])


@pytest.fixture(scope="module")
def math_contract_address(math_contract, address_conversion_func):
    return address_conversion_func(math_contract.address)


@pytest.fixture(scope="module")
def emitter_contract(web3, emitter_contract_factory, node_fixture_data):
    return emitter_contract_factory(address=node_fixture_data['emitter_address'])


@pytest.fixture(scope="module")
def emitter_contract_address(emitter_contract, address_conversion_func):
    return address_conversion_func(emitter_contract.address)


@pytest.fixture
def unlocked_account(web3, unlockable_account, unlockable_account_pw):
    web3.node.personal.unlock_account(unlockable_account, unlockable_account_pw)
    yield unlockable_account
    web3.node.personal.lock_account(unlockable_account)


@pytest.fixture(scope='module')
def unlockable_account_pw(node_fixture_data):
    return node_fixture_data['keyfile_pw']


@pytest.fixture(scope="module")
def unlockable_account(web3, coinbase):
    yield coinbase


@pytest.fixture()
def unlockable_account_dual_type(unlockable_account, address_conversion_func):
    return address_conversion_func(unlockable_account)


@pytest.yield_fixture
def unlocked_account_dual_type(web3, unlockable_account_dual_type, unlockable_account_pw):
    web3.node.personal.unlock_account(unlockable_account_dual_type, unlockable_account_pw)
    yield unlockable_account_dual_type
    web3.node.personal.lock_account(unlockable_account_dual_type)


@pytest.fixture(scope="module")
def funded_account_for_raw_txn(node_fixture_data):
    account = node_fixture_data['raw_txn_account']
    assert is_bech32_address(account)
    return account


@pytest.fixture(scope="module")
def empty_block(web3, node_fixture_data):
    block = web3.platon.get_block(node_fixture_data['empty_block_hash'])
    assert is_dict(block)
    return block


@pytest.fixture(scope="module")
def block_with_txn(web3, node_fixture_data):
    block = web3.platon.get_block(node_fixture_data['block_with_txn_hash'])
    assert is_dict(block)
    return block


@pytest.fixture(scope="module")
def mined_txn_hash(node_fixture_data):
    return node_fixture_data['mined_txn_hash']


@pytest.fixture(scope="module")
def block_with_txn_with_log(web3, node_fixture_data):
    block = web3.platon.get_block(node_fixture_data['block_hash_with_log'])
    assert is_dict(block)
    return block


@pytest.fixture(scope="module")
def txn_hash_with_log(node_fixture_data):
    return node_fixture_data['txn_hash_with_log']


@pytest.fixture(scope="module")
def block_hash_revert_no_msg(node_fixture_data):
    return node_fixture_data['block_hash_revert_no_msg']


@pytest.fixture(scope="module")
def block_hash_revert_with_msg(node_fixture_data):
    return node_fixture_data['block_hash_revert_with_msg']


@pytest.fixture(scope="module")
def revert_contract(web3, revert_contract_factory, node_fixture_data):
    return revert_contract_factory(address=node_fixture_data['revert_address'])
