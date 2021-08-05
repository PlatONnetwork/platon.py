import pytest

from platon_utils.toolz import (
    identity,
)

from platon._utils.method_formatters import (
    raise_block_not_found,
)
from platon.exceptions import (
    BlockNotFound,
    ContractLogicError,
)

ERROR_RESPONSE = {
    'jsonrpc': '2.0',
    'error': {
        'code': -32000,
        'message': 'Requested block number is in a range that is not available yet, '
                   'because the ancient block sync is still in progress.'
    }
}


NONE_RESPONSE = {"jsonrpc": "2.0", "id": 1, "result": None}


def raise_contract_logic_error(response):
    raise ContractLogicError


@pytest.mark.parametrize(
    'response,params,error_formatters,null_result_formatters,error',
    [
        (
            # Error response with no result formatters raises a ValueError
            ERROR_RESPONSE,
            (),
            identity,
            identity,
            ValueError,
        ),
        (
            # Error response with error formatters raises error in formatter
            ERROR_RESPONSE,
            (),
            raise_contract_logic_error,
            identity,
            ContractLogicError,
        ),
        (
            # Error response with no error formatters raises ValueError
            ERROR_RESPONSE,
            (),
            identity,
            raise_block_not_found,
            ValueError,
        ),
        (
            # None result raises error if there is a null_result_formatter
            NONE_RESPONSE,
            (),
            identity,
            raise_block_not_found,
            BlockNotFound,
        ),
        (
            # Params are handled with a None result
            NONE_RESPONSE,
            ('0x03',),
            identity,
            raise_block_not_found,
            BlockNotFound,
        ),
    ],
)
def test_formatted_response_raises_errors(web3,
                                          response,
                                          params,
                                          error_formatters,
                                          null_result_formatters,
                                          error):
    with pytest.raises(error):
        web3.manager.formatted_response(response,
                                        params,
                                        error_formatters,
                                        null_result_formatters)


@pytest.mark.parametrize(
    'response,params,error_formatters,null_result_formatters,expected',
    [
        (
            # Response with a result of None doesn't raise if there is no null result formatter
            NONE_RESPONSE,
            ('0x03'),
            identity,
            identity,
            NONE_RESPONSE['result'],
        ),
    ],
)
def test_formatted_response(response,
                            web3,
                            params,
                            error_formatters,
                            null_result_formatters,
                            expected):

    formatted_resp = web3.manager.formatted_response(response,
                                                     params,
                                                     error_formatters,
                                                     null_result_formatters)
    assert formatted_resp == expected
