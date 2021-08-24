from platon.types import InnerFn
from platon.inner_contract import (
    InnerContract,
)


class Restricting(InnerContract):
    _HEX_ADDRESS = '0x1000000000000000000000000000000000000001'

    def create_restricting(self, release_address, plans):
        """
        Create a restricting

        :param release_address: released to account
        :param plans: a list of restricting plan, for example:
            [{'Epoch': 2, 'Amount': Web3.toWei(1, 'ether')}, {'Epoch': 8, 'Amount': Web3.toWei(3, 'ether')}]

            restricting plan is defined as follows:
            {
                Epoch: int   # the amount will be released to release address when the epoch ends
                Amount: Wei  # restricting amount
            }
        """
        kwargs = locals()
        kwargs['plans'] = [list(plan.values()) for plan in plans]
        return self.function_processor(InnerFn.restricting_createRestricting, kwargs)

    def get_restricting_info(self, release_address):
        """
        Get the restricting information.

        :param release_address: release address for the restricting
        """
        return self.function_processor(InnerFn.restricting_getRestrictingInfo, locals())
