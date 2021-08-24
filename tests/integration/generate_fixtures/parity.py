import contextlib
import json
import os
import pprint
import shutil
import sys
import time

from platon_utils import (
    to_text,
)
from platon_utils.toolz import (
    merge,
)

import common
import platon
from tests.utils import (
    get_open_port,
)
from platon import Web3

CHAIN_CONFIG = {
    "name": "CrossClient",
    "dataDir": "CrossClient",
    "engine": {
        "Platonhash": {
            "params": {
                "minimumDifficulty": "0x020000",
                "difficultyBoundDivisor": "0x0800",
                "durationLimit": "0x0d",
                "blockReward": "0x1bc16d674ec80000",
                "difficultyBombDelays": {
                    "0x0": "0x1e8480",
                },
                "homesteadTransition": 0,
                "eip100bTransition": 0,
            }
        }
    },
    "params": {
        "gasLimitBoundDivisor": "0x0400",
        "registrar": "0x81a4b044831c4f12ba601adb9274516939e9b8a2",
        #  Tangerine Whistle
        "eip150Transition": 0,
        #  Spurious Dragon
        "eip160Transition": 0,
        "eip161abcTransition": 0,
        "eip161dTransition": 0,
        "eip155Transition": 0,
        #  Byzantium
        "eip140Transition": 0,
        "eip211Transition": 0,
        "eip214Transition": 0,
        "eip658Transition": 0,
        #  Constantinople
        "eip145Transition": 0,
        "eip1014Transition": 0,
        "eip1052Transition": 0,
        "eip1283Transition": 0,
        #  TODO: Petersburg
        #  "eip1283DisableTransition": 0,
        #  TODO: Istanbul
        #  "eip1283ReenableTransition": 0,
        #  "eip1344Transition": 0,
        #  "eip1884Transition": 0,
        #  "eip2028Transition": 0,
        "accountStartNonce": "0x0",
        "maximumExtraDataSize": "0x20",
        "minGasLimit": "0x1388",
        "networkID": "0x776562337079",  # the string 'web3py' as a hex string
        "eip98Transition": "0x7fffffffffffffff",
    },
    "genesis": {
        "seal": {
            "platon": {
                "nonce": "0x0000000000000042",
                "mixHash": "0x0000000000000000000000000000000000000000000000000000000000000000"
            }
        },
        "difficulty": "0x10000",
        "author": common.COINBASE,
        "timestamp": "0x00",
        "parentHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
        "extraData": "0x3535353535353535353535353535353535353535353535353535353535353535",
        "gasLimit": "0x1000000"
    },
    "accounts": {
        common.COINBASE: {"balance": "1000000000000000000000000000", "nonce": "0"},
        common.UNLOCKABLE_ACCOUNT: {"balance": "1000000000000000000000000000", "nonce": "0"},
        common.RAW_TXN_ACCOUNT: {"balance": "1000000000000000000000000000", "nonce": "0"},
        "0000000000000000000000000000000000000001": {
            "balance": "0x1",
            "builtin": {
                "name": "ecrecover",
                "pricing": {"linear": {"base": 3000, "word": 0}}
            }
        },
        "0000000000000000000000000000000000000002": {
            "balance": "0x1",
            "builtin": {
                "name": "sha256",
                "pricing": {"linear": {"base": 60, "word": 12}}
            }
        },
        "0000000000000000000000000000000000000003": {
            "balance": "0x1",
            "builtin": {
                "name": "ripemd160",
                "pricing": {"linear": {"base": 600, "word": 120}}
            }
        },
        "0000000000000000000000000000000000000004": {
            "balance": "0x1",
            "builtin": {
                "name": "identity",
                "pricing": {"linear": {"base": 15, "word": 3}}
            }
        },
        "0000000000000000000000000000000000000005": {
            "balance": "0x1",
            "builtin": {
                "name": "modexp",
                "pricing": {"modexp": {"divisor": 20}}
            }
        },
        "0000000000000000000000000000000000000006": {
            "balance": "0x1",
            "builtin": {
                "name": "alt_bn128_add",
                "activate_at": "0x7530",
                "pricing": {"linear": {"base": 500, "word": 0}}
            }
        },
    }
}


def get_parity_binary():
    """
    If generating a fixture from a local binary, update this value to that bin, e.g.,
    return '/Users/xzy/Downloads/openplaton-2.5.13/target/release/parity'
    """
    return 'parity'


@contextlib.contextmanager
def get_parity_process(
        parity_binary,
        datadir,
        ipc_path,
        keys_path,
        chain_config_file_path,
        parity_port):

    run_command = (
        parity_binary,
        '--base-path', datadir,
        '--ipc-path', ipc_path,
        '--no-ws',
        '--no-warp',
        '--chain', chain_config_file_path,
        '--keys-path', keys_path,
        '--jsonrpc-apis', 'all',
        '--jsonrpc-port', parity_port,
        '--fat-db', 'on',
    )
    print(' '.join(run_command))
    try:
        proc = common.get_process(run_command)
        yield proc
    finally:
        common.kill_proc_gracefully(proc)
        output, errors = proc.communicate()
        print(
            "Parity Process Exited:\n"
            "stdout:{0}\n\n"
            "stderr:{1}\n\n".format(
                to_text(output),
                to_text(errors),
            )
        )


@contextlib.contextmanager
def parity_export_blocks_process(
        parity_binary,
        datadir,
        chain_config_file_path,
        parity_port):

    run_command = (
        parity_binary,
        'export',
        'blocks', os.path.join(datadir, 'blocks_export.rlp'),
        '--base-path', datadir,
        '--no-ws',
        '--no-warp',
        '--chain', chain_config_file_path,
        '--jsonrpc-apis', 'all',
        '--jsonrpc-port', parity_port,
        '--fat-db', 'on',
    )
    print(' '.join(run_command))
    try:
        proc = common.get_process(run_command)
        yield proc
    finally:
        time.sleep(10)
        common.kill_proc_gracefully(proc)
        output, errors = proc.communicate()
        print(
            "Parity Process Exited:\n"
            "stdout:{0}\n\n"
            "stderr:{1}\n\n".format(
                to_text(output),
                to_text(errors),
            )
        )


def generate_parity_fixture(destination_dir):
    """
    The parity fixture generation strategy is to start a node client with
    existing fixtures copied into a temp data_dir.  Then a parity client
    is started is peered with the node client.
    """
    with contextlib.ExitStack() as stack:

        node_datadir = stack.enter_context(common.tempdir())

        node_port = get_open_port()

        node_ipc_path_dir = stack.enter_context(common.tempdir())
        node_ipc_path = os.path.join(node_ipc_path_dir, 'node.ipc')

        node_keystore_dir = os.path.join(node_datadir, 'keystore')
        common.ensure_path_exists(node_keystore_dir)
        node_keyfile_path = os.path.join(node_keystore_dir, common.KEYFILE_FILENAME)
        with open(node_keyfile_path, 'w') as keyfile:
            keyfile.write(common.KEYFILE_DATA)

        genesis_file_path = os.path.join(node_datadir, 'genesis.json')
        with open(genesis_file_path, 'w') as genesis_file:
            genesis_file.write(json.dumps(common.GENESIS_DATA))

        stack.enter_context(
            common.get_node_process(
                common.get_node_binary(),
                node_datadir,
                genesis_file_path,
                node_ipc_path,
                node_port,
                str(CHAIN_CONFIG['params']['networkID'])
            )
        )
        # set up fixtures
        common.wait_for_socket(node_ipc_path)
        web3_node = Web3(Web3.IPCProvider(node_ipc_path))
        chain_data = platon.setup_chain_state(web3_node)
        fixture_block_count = web3_node.platon.block_number

        datadir = stack.enter_context(common.tempdir())

        keystore_dir = os.path.join(datadir, 'keys')
        os.makedirs(keystore_dir, exist_ok=True)
        parity_keyfile_path = os.path.join(keystore_dir, common.KEYFILE_FILENAME)
        with open(parity_keyfile_path, 'w') as keyfile:
            keyfile.write(common.KEYFILE_DATA)

        chain_config_file_path = os.path.join(datadir, 'chain_config.json')
        with open(chain_config_file_path, 'w') as chain_file:
            chain_file.write(json.dumps(CHAIN_CONFIG))

        parity_ipc_path_dir = stack.enter_context(common.tempdir())
        parity_ipc_path = os.path.join(parity_ipc_path_dir, 'jsonrpc.ipc')

        parity_port = get_open_port()
        parity_binary = get_parity_binary()

        parity_proc = stack.enter_context(get_parity_process(  # noqa: F841
            parity_binary=parity_binary,
            datadir=datadir,
            ipc_path=parity_ipc_path,
            keys_path=keystore_dir,
            chain_config_file_path=chain_config_file_path,
            parity_port=parity_port,
        ))

        common.wait_for_socket(parity_ipc_path)
        web3 = Web3(Web3.IPCProvider(parity_ipc_path))

        time.sleep(10)
        connect_nodes(web3, web3_node)
        time.sleep(10)
        wait_for_chain_sync(web3, fixture_block_count)

        static_data = {
            'raw_txn_account': common.RAW_TXN_ACCOUNT,
            'keyfile_pw': common.KEYFILE_PW,
        }
        pprint.pprint(merge(chain_data, static_data))

        shutil.copytree(datadir, destination_dir)

        parity_proc = stack.enter_context(parity_export_blocks_process(  # noqa: F841
            parity_binary=parity_binary,
            datadir=destination_dir,
            chain_config_file_path=os.path.join(destination_dir, 'chain_config.json'),
            parity_port=parity_port,
        ))

        time.sleep(10)
        shutil.make_archive(destination_dir, 'zip', destination_dir)
        shutil.rmtree(destination_dir)


def connect_nodes(w3_parity, w3_secondary):
    parity_peers = w3_parity.parity.net_peers()
    parity_enode = w3_parity.parity.enode()
    secondary_node_info = w3_secondary.node.admin.node_info()
    if secondary_node_info['id'] not in (node.get('id', tuple()) for node in parity_peers['peers']):
        w3_secondary.node.admin.add_peer(parity_enode)


def wait_for_chain_sync(web3, target):
    start_time = time.time()
    while time.time() < start_time + 120:
        current_block_number = web3.platon.block_number
        if current_block_number >= target:
            break
        else:
            time.sleep(0.1)
    else:
        raise ValueError("Not synced after wait period")


if __name__ == '__main__':
    fixture_dir = sys.argv[1]
    generate_parity_fixture(fixture_dir)
