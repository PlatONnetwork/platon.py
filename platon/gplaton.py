from platon._utils.admin import (
    add_peer,
    data_dir,
    node_info,
    peers,
    start_rpc,
    start_ws,
    stop_rpc,
    stop_ws,
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


class GplatonPersonal(Module):
    """
    https://github.com/platonnetwork/platon-go/wiki/management-apis#personal
    """
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


class GplatonTxPool(Module):
    """
    https://github.com/platonnetwork/platon-go/wiki/Management-APIs#txpool
    """
    content = content
    inspect = inspect
    status = status


class GplatonAdmin(Module):
    """
    https://github.com/platonnetwork/platon-go/wiki/Management-APIs#admin
    """
    peers = peers
    data_dir = data_dir
    add_peer = add_peer
    node_info = node_info
    start_rpc = start_rpc
    start_ws = start_ws
    stop_ws = stop_ws
    stop_rpc = stop_rpc


class GplatonMiner(Module):
    """
    https://github.com/platonnetwork/platon-go/wiki/Management-APIs#miner
    """
    make_dag = make_dag
    set_extra = set_extra
    set_etherbase = set_etherbase
    set_gas_price = set_gas_price
    start = start
    stop = stop
    start_auto_dag = start_auto_dag
    stop_auto_dag = stop_auto_dag


class Gplaton(Module):
    personal: GplatonPersonal
    admin: GplatonAdmin
