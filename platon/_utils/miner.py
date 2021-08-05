from typing import (
    Callable,
)

from platon_typing import (
    Bech32Address,
)

from platon._utils.rpc_abi import (
    RPC,
)
from platon.method import (
    Method,
    default_root_munger,
)
from platon.types import (
    BlockNumber,
    Wei,
)

make_dag: Method[Callable[[BlockNumber], bool]] = Method(
    RPC.miner_makeDag,
    mungers=[default_root_munger],
)


set_extra: Method[Callable[[str], bool]] = Method(
    RPC.miner_setExtra,
    mungers=[default_root_munger],
)


set_etherbase: Method[Callable[[Bech32Address], bool]] = Method(
    RPC.miner_setEtherbase,
    mungers=[default_root_munger],
)


set_gas_price: Method[Callable[[Wei], bool]] = Method(
    RPC.miner_setGasPrice,
    mungers=[default_root_munger],
)


start: Method[Callable[[int], bool]] = Method(
    RPC.miner_start,
    mungers=[default_root_munger],
)


stop: Method[Callable[[], bool]] = Method(
    RPC.miner_stop,
    mungers=None,
)


start_auto_dag: Method[Callable[[], bool]] = Method(
    RPC.miner_startAutoDag,
    mungers=None,
)


stop_auto_dag: Method[Callable[[], bool]] = Method(
    RPC.miner_stopAutoDag,
    mungers=None,
)
