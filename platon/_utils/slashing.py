from typing import Union

from platon_typing import NodeID, HexStr
from platon_typing.evm import BlockNumber

from platon.types import InnerFn
from platon.inner_contract import (
    InnerContract,
)


class Slashing(InnerContract):
    _HEX_ADDRESS = '0x1000000000000000000000000000000000000004'

    def report_duplicate_sign(self, report_type: int, data: str):
        """ Report duplicate sign

        :param report_type: duplicate sign type, prepareBlock: 1, prepareVote: 2, viewChange: 3
        :param data: a JSON string of evidence, format reference RPC platon_Evidences
        """
        return self.function_processor(InnerFn.slashing_reportDuplicateSign, locals())

    def check_duplicate_sign(self,
                             report_type: int,
                             node_id: Union[NodeID, HexStr],
                             block_number: BlockNumber,
                             ):
        """
        Query whether the node has been reported duplicate-sign

        :param report_type: duplicate sign type, prepareBlock: 1, prepareVote: 2, viewChange: 3
        :param node_id: node id to report
        :param block_number: duplicate-signed block number
        """
        return self.function_processor(InnerFn.slashing_checkDuplicateSign, locals())
