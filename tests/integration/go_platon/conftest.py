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

GPLATON_FIXTURE_ZIP = 'gplaton-1.10.4-fixture.zip'


@pytest.fixture(scope='module')
def gplaton_binary():
    from gplaton.install import (
        get_executable_path,
        install_gplaton,
    )

    if 'GPLATON_BINARY' in os.environ:
        return os.environ['GPLATON_BINARY']
    elif 'GPLATON_VERSION' in os.environ:
        gplaton_version = os.environ['GPLATON_VERSION']
        _gplaton_binary = get_executable_path(gplaton_version)
        if not os.path.exists(_gplaton_binary):
            install_gplaton(gplaton_version)
        assert os.path.exists(_gplaton_binary)
        return _gplaton_binary
    else:
        return 'gplaton'


def absolute_datadir(directory_name):
    return os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        '..',
        directory_name,
    ))


@pytest.fixture(scope="module")
def get_gplaton_version(gplaton_binary):
    from gplaton import get_gplaton_version
    return get_gplaton_version(gplaton_executable=os.path.expanduser(gplaton_binary))


@pytest.fixture(scope="module")
def base_gplaton_command_arguments(gplaton_binary, datadir):
    return (
        gplaton_binary,
        '--data_dir', str(datadir),
        '--nodiscover',
        '--fakepow',
    )


@pytest.fixture(scope="module")
def gplaton_zipfile_version(get_gplaton_version):
    if get_gplaton_version.major == 1 and get_gplaton_version.minor == 10:
        return GPLATON_FIXTURE_ZIP
    raise AssertionError("Unsupported gplaton version")


@pytest.fixture(scope='module')
def datadir(tmpdir_factory, gplaton_zipfile_version):
    zipfile_path = absolute_datadir(gplaton_zipfile_version)
    base_dir = tmpdir_factory.mktemp('platon')
    tmp_datadir = os.path.join(str(base_dir), 'data_dir')
    with zipfile.ZipFile(zipfile_path, 'r') as zip_ref:
        zip_ref.extractall(tmp_datadir)
    return tmp_datadir


@pytest.fixture(scope="module")
def gplaton_fixture_data(datadir):
    config_file_path = Path(datadir) / 'config.json'
    return json.loads(config_file_path.read_text())


@pytest.fixture(scope='module')
def genesis_file(datadir):
    genesis_file_path = os.path.join(datadir, 'genesis.json')
    return genesis_file_path


@pytest.fixture(scope='module')
def gplaton_process(gplaton_binary, datadir, genesis_file, gplaton_command_arguments):
    init_datadir_command = (
        gplaton_binary,
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
        gplaton_command_arguments,
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
            "Gplaton Process Exited:\n"
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
def math_contract_deploy_txn_hash(gplaton_fixture_data):
    return gplaton_fixture_data['math_deploy_txn_hash']


@pytest.fixture(scope="module")
def math_contract(web3, math_contract_factory, gplaton_fixture_data):
    return math_contract_factory(address=gplaton_fixture_data['math_address'])


@pytest.fixture(scope="module")
def math_contract_address(math_contract, address_conversion_func):
    return address_conversion_func(math_contract.address)


@pytest.fixture(scope="module")
def emitter_contract(web3, emitter_contract_factory, gplaton_fixture_data):
    return emitter_contract_factory(address=gplaton_fixture_data['emitter_address'])


@pytest.fixture(scope="module")
def emitter_contract_address(emitter_contract, address_conversion_func):
    return address_conversion_func(emitter_contract.address)


@pytest.fixture
def unlocked_account(web3, unlockable_account, unlockable_account_pw):
    web3.gplaton.personal.unlock_account(unlockable_account, unlockable_account_pw)
    yield unlockable_account
    web3.gplaton.personal.lock_account(unlockable_account)


@pytest.fixture(scope='module')
def unlockable_account_pw(gplaton_fixture_data):
    return gplaton_fixture_data['keyfile_pw']


@pytest.fixture(scope="module")
def unlockable_account(web3, coinbase):
    yield coinbase


@pytest.fixture()
def unlockable_account_dual_type(unlockable_account, address_conversion_func):
    return address_conversion_func(unlockable_account)


@pytest.yield_fixture
def unlocked_account_dual_type(web3, unlockable_account_dual_type, unlockable_account_pw):
    web3.gplaton.personal.unlock_account(unlockable_account_dual_type, unlockable_account_pw)
    yield unlockable_account_dual_type
    web3.gplaton.personal.lock_account(unlockable_account_dual_type)


@pytest.fixture(scope="module")
def funded_account_for_raw_txn(gplaton_fixture_data):
    account = gplaton_fixture_data['raw_txn_account']
    assert is_bech32_address(account)
    return account


@pytest.fixture(scope="module")
def empty_block(web3, gplaton_fixture_data):
    block = web3.platon.get_block(gplaton_fixture_data['empty_block_hash'])
    assert is_dict(block)
    return block


@pytest.fixture(scope="module")
def block_with_txn(web3, gplaton_fixture_data):
    block = web3.platon.get_block(gplaton_fixture_data['block_with_txn_hash'])
    assert is_dict(block)
    return block


@pytest.fixture(scope="module")
def mined_txn_hash(gplaton_fixture_data):
    return gplaton_fixture_data['mined_txn_hash']


@pytest.fixture(scope="module")
def block_with_txn_with_log(web3, gplaton_fixture_data):
    block = web3.platon.get_block(gplaton_fixture_data['block_hash_with_log'])
    assert is_dict(block)
    return block


@pytest.fixture(scope="module")
def txn_hash_with_log(gplaton_fixture_data):
    return gplaton_fixture_data['txn_hash_with_log']


@pytest.fixture(scope="module")
def block_hash_revert_no_msg(gplaton_fixture_data):
    return gplaton_fixture_data['block_hash_revert_no_msg']


@pytest.fixture(scope="module")
def block_hash_revert_with_msg(gplaton_fixture_data):
    return gplaton_fixture_data['block_hash_revert_with_msg']


@pytest.fixture(scope="module")
def revert_contract(web3, revert_contract_factory, gplaton_fixture_data):
    return revert_contract_factory(address=gplaton_fixture_data['revert_address'])
