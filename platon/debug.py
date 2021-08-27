from typing import (
    Callable,
)
from platon.method import (
    Method,
)

from platon._utils.rpc_abi import (
    RPC,
)
from platon.module import (
    Module,
)


class Debug(Module):

    economic_config: Method[Callable[[], str]] = Method(RPC.debug_economicConfig)
    get_wait_slashing_node_list: Method[Callable[[], str]] = Method(RPC.debug_getWaitSlashingNodeList)
    get_bad_blocks: Method[Callable[[], str]] = Method(RPC.debug_getBadBlocks)