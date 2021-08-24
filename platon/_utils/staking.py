from typing import Union

from platon_typing import NodeID, URI, BLSPubkey, BLSSignature, HexStr, Decodable
from platon_typing.evm import Bech32Address, BlockNumber

from platon.types import InnerFn
from platon.types import Wei, Version
from platon.inner_contract import (
    InnerContract, bubble_dict,
)


class Staking(InnerContract):
    _HEX_ADDRESS = '0x1000000000000000000000000000000000000002'

    def create_staking(self,
                       balance_type: int,  # todo: add rangge int type
                       benefit_address: Bech32Address,
                       node_id: Union[NodeID, HexStr],
                       external_id: str,
                       node_name: str,
                       website: URI,
                       details: str,
                       amount: Wei,
                       reward_per: int,
                       node_version: Version,
                       version_sign: Union[Decodable, HexStr],  # todo: noqa
                       bls_pubkey: Union[BLSPubkey, HexStr],
                       bls_proof: Union[BLSSignature, HexStr],
                       ):
        """ Initiate Staking
        :param balance_type: Indicates whether the account free amount or the account's lock amount is used for staking, 0: free amount; 1: lock amount;
                    2: Give priority to lock amount , use free amount provided that staking amount over lock amount
        :param benefit_address: Income account for accepting block rewards and staking rewards
        :param node_id: The idled node Id (also called the candidate's node Id)
        :param external_id: External Id (with length limit, Id for the third party to pull the node description)
        :param node_name: The name of the staking node (with a length limit indicating the name of the node)
        :param website: The third-party home page of the node (with a length limit indicating the home page of the node)
        :param details: Description of the node (with a length limit indicating the description of the node)
        :param amount: staking von (unit:von, 1LAT = 10**18 von)
        :param node_version: The real version of the program, admin_getProgramVersion
        :param version_sign: The real version of the program is signed, admin_getProgramVersion
        :param bls_pubkey: Bls public key
        :param bls_proof: Proof of bls, obtained by pulling the proof interface, admin_getSchnorrNIZKProve
        :param reward_per: Proportion of the reward share obtained from the commission, using BasePoint 1BP = 0.01%
        """
        return self.function_processor(InnerFn.staking_createStaking, locals())

    def edit_candidate(self,
                       node_id: Union[NodeID, HexStr],
                       benefit_address: Bech32Address = None,
                       external_id: str = None,
                       node_name: str = None,
                       website: str = None,
                       details: str = None,
                       reward_per: int = None,
                       ):
        """ Modify staking information
        :param benefit_address: Income account for accepting block rewards and staking rewards
        :param node_id: The idled node Id (also called the candidate's node Id)
        :param external_id: External Id (with length limit, Id for the third party to pull the node description)
        :param node_name: The name of the staking node (with a length limit indicating the name of the node)
        :param website: The third-party home page of the node (with a length limit indicating the home page of the node)
        :param details: Description of the node (with a length limit indicating the description of the node)
        :param reward_per: Proportion of the reward share obtained from the commission, using BasePoint 1BP = 0.01%
        """
        # Put benefit address at the top to fit the parameter order
        kwargs = bubble_dict(locals(), 'benefit_address')
        return self.function_processor(InnerFn.staking_editCandidate, kwargs)

    def increase_staking(self,
                         balance_type: int,
                         node_id: Union[NodeID, HexStr],
                         amount: Wei,
                         ):
        """
        Increase staking
        :param balance_type: Indicates whether the account free amount or the account's lock amount is used for staking, 0: free amount; 1: lock amount;
                    2: Give priority to lock amount , use free amount provided that staking amount over lock amount
        :param node_id: The idled node Id (also called the candidate's node Id)
        :param amount: staking von (unit:von, 1LAT = 10**18 von)
        """
        return self.function_processor(InnerFn.staking_increaseStaking, locals())

    def withdrew_staking(self, node_id: Union[NodeID, HexStr]):
        """
        Withdrawal of staking (one-time initiation of all cancellations, multiple arrivals)
        :param node_id: The idled node Id (also called the candidate's node Id)
        """
        return self.function_processor(InnerFn.staking_withdrewStaking, locals())

    def get_verifier_list(self):
        """
        Query the certified queue for the current billing cycle
        """
        return self.function_processor(InnerFn.staking_getVerifierList, locals(), is_call=True)

    def get_validator_list(self):
        """
        Query the list of certified for the current consensus cycle
        """
        return self.function_processor(InnerFn.staking_getValidatorList, locals(), is_call=True)

    def get_candidate_list(self):
        """
        Query all real-time candidate lists
        """
        return self.function_processor(InnerFn.staking_getCandidateList, locals(), is_call=True)

    def get_candidate_info(self, node_id: Union[NodeID, HexStr]):
        """
        Query the staking information of the current node
        :param node_id: Verifier's node ID
        """
        return self.function_processor(InnerFn.staking_getCandidateInfo, locals(), is_call=True)

    def get_package_reward(self):
        """

        """
        return self.function_processor(InnerFn.staking_getPackageReward, locals(), is_call=True)

    def get_staking_reward(self):
        """

        """
        return self.function_processor(InnerFn.staking_getStakingReward, locals(), is_call=True)

    def get_avg_pack_time(self):
        """

        """
        return self.function_processor(InnerFn.staking_getAvgPackTime, locals(), is_call=True)
