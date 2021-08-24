from typing import Union

from platon_typing import NodeID, HexStr
from platon_typing.evm import Bech32Address, BlockNumber

from platon.types import InnerFn
from platon.inner_contract import (
    InnerContract,
)


class _DelegatePart(InnerContract):
    _HEX_ADDRESS = '0x1000000000000000000000000000000000000002'

    def delegate(self,
                 balance_type: int,
                 node_id: Union[NodeID, HexStr],
                 amount: int
                 ):
        """
        Initiate delegate
        :param balance_type: Indicates whether the account free amount or the account's lock amount is used for delegate, 0: free amount; 1: lock amount
        :param node_id: The idled node Id (also called the candidate's node Id)
        :param amount: Amount of delegate (unit:von, 1LAT = 10**18 von)
        """
        return self.function_processor(InnerFn.delegate_delegate, locals())

    def withdrew_delegate(self,
                          staking_block_number: BlockNumber,
                          node_id: Union[NodeID, HexStr],
                          amount: int
                          ):
        """
        Reduction/revocation of delegate (all reductions are revoked)
        :param staking_block_number: A unique indication of a pledge of a node
        :param node_id: The idled node Id (also called the candidate's node Id)
        :param amount: The amount of the entrusted reduction (unit:von, 1LAT = 10**18 von)
        """
        return self.function_processor(InnerFn.delegate_withdrewDelegation, locals())

    def redeem_delegation(self,
                          staking_block_number: BlockNumber,
                          node_id: Union[NodeID, HexStr],
                          amount: int
                          ):
        return self.function_processor(InnerFn.delegate_redeemDelegation, locals())

    def get_delegate_list(self, delegate_address: Bech32Address):
        """
        Query the NodeID and pledge ID of the node entrusted by the current account address
        :param delegate_address: Client's account address
        """
        return self.function_processor(InnerFn.delegate_getDelegateList, locals(), is_call=True)

    def get_delegate_info(self,
                          staking_block_number: BlockNumber,
                          delegate_address: Bech32Address,
                          node_id: Union[NodeID, HexStr]
                          ):
        """
        Query current single delegation information
        :param staking_block_number: Block height at the time of staking
        :param delegate_address: Client's account address
        :param node_id: Verifier's node ID
        """
        return self.function_processor(InnerFn.staking_getCandidateInfo, locals(), is_call=True)


class _DelegateReward(InnerContract):
    _HEX_ADDRESS = '0x1000000000000000000000000000000000000006'

    def withdraw_delegate_reward(self):
        """
        withdraw all delegate rewards for sending address
        """
        return self.function_processor(InnerFn.delegate_withdrawDelegateReward, locals())

    def get_delegate_reward(self,
                            address: Bech32Address,
                            node_ids: list = [],
                            ):
        """
        get the delegate rewards for account by nodes
        """
        return self.function_processor(InnerFn.delegate_getDelegateReward, locals())


class Delegate(_DelegatePart, _DelegateReward):
    pass
