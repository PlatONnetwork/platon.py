import copy
from typing import Optional, Any, cast, TYPE_CHECKING
from collections import Iterable

import rlp
from platon.exceptions import ContractLogicError
from platon_typing import HexStr, Bech32Address
from platon_utils import to_bech32_address
from platon._utils.empty import empty
from platon._utils.rpc_abi import apply_abi_formatters_to_dict
from platon._utils.transactions import fill_transaction_defaults
from platon._utils.argument_formatter import INNER_CONTRACT_ABIS, INNER_CONTRACT_NORMALIZERS, DEFAULT_PARAM_ABIS
from platon.types import TxParams, BlockIdentifier, CallOverrideParams, FunctionIdentifier

if TYPE_CHECKING:
    from platon import Web3


class InnerContract:
    _HEX_ADDRESS = None
    _address = None
    _contract_function = None

    # If you want to get the result of the transaction, please set it to True,
    # if you only want to get the transaction hash, please set it to False
    # is_analyze = False

    def __init__(self, web3: "Web3"):
        self.web3: Web3 = web3

    @property
    def address(self):
        if not self._address:
            self._address = to_bech32_address(self._HEX_ADDRESS, self.web3.hrp)
        return self._address

    @property
    def contract_function(self):
        if not self._contract_function:
            self._contract_function = InnerContractFunction(self.web3, self.address)
        return self._contract_function

    def function_processor(self, func_type: FunctionIdentifier, kwargs: dict, is_call: bool = False) -> callable:
        self.process_kwargs(kwargs)
        if is_call:
            return self.contract_function(func_type, kwargs).call()
        return self.contract_function(func_type, kwargs)

    @staticmethod
    def process_kwargs(kwargs: dict):
        kwargs.pop("self")
        for key, value in kwargs.items():
            if type(value) in (tuple, list, dict):
                raise ValueError(
                    "Invalid argument: {}, the value cannot be a tuple, list, or dictionary".format(key))


class InnerContractFunction:
    func_id: FunctionIdentifier = None
    kwargs: dict = None

    def __init__(self, web3: "Web3", address: Bech32Address):
        self.web3: Web3 = web3
        self.address: Bech32Address = address

    def __call__(self, func_type: FunctionIdentifier, kwargs: dict) -> 'InnerContractFunction':
        clone = copy.copy(self)
        clone.func_id = func_type
        if kwargs is None:
            clone.kwargs = {}
        else:
            clone.kwargs = kwargs

        return clone

    def call(self,
             transaction: Optional[TxParams] = None,
             block_identifier: BlockIdentifier = 'latest',
             state_override: Optional[CallOverrideParams] = None,
             ) -> Any:

        if transaction is None:
            call_transaction: TxParams = {}
        else:
            call_transaction = cast(TxParams, dict(**transaction))

        if 'data' in call_transaction:
            raise ValueError("Cannot set data in call transaction")

        if 'to' in call_transaction:
            raise ValueError("Cannot set to address in contract call transaction")

        if self.address:
            call_transaction.setdefault('to', self.address)

        if self.web3.platon.default_account is not empty:
            # type ignored b/c check prevents an empty default_account
            call_transaction.setdefault('from', self.web3.platon.default_account)  # type: ignore

        if 'to' not in call_transaction:
            raise ValueError(
                "Please ensure that this inner contract instance has an address."
            )

        call_transaction['data'] = self._encode_transaction_data()

        # todo: format the return data
        return_data = self.web3.platon.call(call_transaction,
                                            block_identifier=block_identifier,
                                            state_override=state_override,
                                            )

        # self._formatter_result()

        return return_data

    def transact(self):
        # todo: wait coding
        pass

    def estimate_gas(self,
                     transaction: Optional[TxParams] = None,
                     block_identifier: Optional[BlockIdentifier] = None
                     ) -> int:
        if transaction is None:
            estimate_transaction: TxParams = {}
        else:
            estimate_transaction = cast(TxParams, dict(**transaction))

        if 'data' in estimate_transaction:
            raise ValueError("Cannot set data in build transaction")

        if 'to' in estimate_transaction:
            raise ValueError("Cannot set to address in contract call build transaction")

        if self.address:
            estimate_transaction.setdefault('to', self.address)

        if 'to' not in estimate_transaction:
            raise ValueError(
                "Please ensure that this inner contract instance has an address."
            )

        estimate_transaction['data'] = self._encode_transaction_data()

        return self.web3.platon.estimate_gas(estimate_transaction, block_identifier)

    def build_transaction(self, transaction: Optional[TxParams] = None) -> TxParams:
        """
                Build the transaction dictionary without sending
            """
        if transaction is None:
            built_transaction: TxParams = {}
        else:
            built_transaction = cast(TxParams, dict(**transaction))

        if 'data' in built_transaction:
            raise ValueError("Cannot set data in build transaction")

        if 'to' in built_transaction:
            raise ValueError("Cannot set to address in contract call build transaction")

        if self.address:
            built_transaction.setdefault('to', self.address)

        if 'to' not in built_transaction:
            raise ValueError(
                "Please ensure that this inner contract instance has an address."
            )

        built_transaction['data'] = self._encode_transaction_data()

        built_transaction = fill_transaction_defaults(self.web3, built_transaction)

        return built_transaction

    def _encode_transaction_data(self) -> HexStr:
        encoded_args = [rlp.encode(self.func_id)]

        self.kwargs = self._formatter_kwargs(self.func_id, kwargs=self.kwargs)
        if self.kwargs:
            # encodes parameters sequentially
            for key, value in self.kwargs.items():
                if value is None:
                    encoded_args.append(b'')
                else:
                    encoded_args.append(rlp.encode(value))

        return rlp.encode(encoded_args)

    @staticmethod
    def _formatter_kwargs(func_id: FunctionIdentifier, kwargs: dict):
        """
        Format transaction so that it can be used correctly during RPC encoding
        """
        kwargs = apply_abi_formatters_to_dict(INNER_CONTRACT_NORMALIZERS,
                                              DEFAULT_PARAM_ABIS,
                                              kwargs)
        function_abis = INNER_CONTRACT_ABIS.get(func_id)
        if function_abis:
            return apply_abi_formatters_to_dict(INNER_CONTRACT_NORMALIZERS, function_abis, kwargs)
        return kwargs

    @staticmethod
    def _formatter_result(func_id: FunctionIdentifier, result: dict):
        """
        Format transaction so that it can be used correctly during RPC encoding
        """
        if type(result) is not dict:
            return result

        if 'Code' not in result.keys() or 'Ret' not in result.keys():
            return result

        # todo: Wait to resolve the return value issue
        # if result.get('Code') != 0:
        #     raise ContractLogicError()

        rets = result.get('Ret')
        if type(rets) is not Iterable:
            rets = [rets]

        if type(rets) is not list:
            try:
                rets = list(rets)
            except Exception:
                raise ValueError(f"Failed to convert value {rets} to list")

        function_abis = INNER_CONTRACT_ABIS.get(func_id)

        for ret in rets:
            kwargs = apply_abi_formatters_to_dict(INNER_CONTRACT_NORMALIZERS,
                                                  DEFAULT_PARAM_ABIS,
                                                  ret,
                                                  )
            if function_abis:
                return apply_abi_formatters_to_dict(INNER_CONTRACT_NORMALIZERS, function_abis, kwargs)
        return kwargs


def bubble_dict(target: dict, *keys: Any):
    copy_dict = copy.copy(target)
    new_dict = dict()
    for key in reversed(keys):
        value = copy_dict.pop(key)
        new_dict.update({value: keys})
    return new_dict.update(copy_dict)
