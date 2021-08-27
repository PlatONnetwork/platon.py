from platon._utils.admin import (
    add_peer,
    rmeove_peer,
    data_dir,
    node_info,
    peers,
    start_rpc,
    start_ws,
    stop_rpc,
    stop_ws,
    import_chain,
    export_chain,
    get_program_version,
    get_schnorr_NIZK_prove,
    set_solc,
)
from platon._utils.miner import (
    make_dag,
    set_etherbase,
    set_extra,
    set_gas_price,
    start,
    start_auto_dag,
    stop,
    stop_auto_dag,
)
from platon._utils.personal import (
    ec_recover,
    import_raw_key,
    list_accounts,
    list_wallets,
    lock_account,
    new_account,
    send_transaction,
    sign,
    sign_typed_data,
    unlock_account,
)
from platon._utils.txpool import (
    content,
    inspect,
    status,
)
from platon.module import (
    Module,
)


class Admin(Module):
    peers = peers
    add_peer = add_peer
    rmeove_peer = rmeove_peer
    data_dir = data_dir
    node_info = node_info
    start_rpc = start_rpc
    start_ws = start_ws
    stop_ws = stop_ws
    stop_rpc = stop_rpc
    import_chain = import_chain
    export_chain = export_chain
    get_program_version = get_program_version
    get_schnorr_NIZK_prove = get_schnorr_NIZK_prove
    set_solc = set_solc


class Miner(Module):
    make_dag = make_dag
    set_extra = set_extra
    set_etherbase = set_etherbase
    set_gas_price = set_gas_price
    start = start
    stop = stop
    start_auto_dag = start_auto_dag
    stop_auto_dag = stop_auto_dag


class Personal(Module):
    ec_recover = ec_recover
    import_raw_key = import_raw_key
    list_accounts = list_accounts
    list_wallets = list_wallets
    lock_account = lock_account
    new_account = new_account
    send_transaction = send_transaction
    sign = sign
    sign_typed_data = sign_typed_data
    unlock_account = unlock_account


class TxPool(Module):
    content = content
    inspect = inspect
    status = status


class Node(Module):
    admin: Admin
    miner: Miner
    personal: Personal
    txpool: TxPool
