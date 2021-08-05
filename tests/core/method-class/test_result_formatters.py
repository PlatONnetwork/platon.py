import pytest

from platon_utils.toolz import (
    compose,
)

from platon import Web3
from platon.method import (
    Method,
)
from platon.middleware.fixture import (
    construct_result_generator_middleware,
)
from platon.module import (
    Module,
)
from platon.providers import (
    BaseProvider,
)


def result_formatter(method, module):
    def formatter(self):
        return 'OKAY'
    return compose(formatter)


class DummyProvider(BaseProvider):
    def make_request(method, params):
        raise NotImplementedError


result_middleware = construct_result_generator_middleware({
    'method_for_test': lambda m, p: 'ok',
})


class ModuleForTest(Module):
    method = Method(
        'method_for_test',
        result_formatters=result_formatter)


@pytest.fixture
def dummy_w3():
    w3 = Web3(
        DummyProvider(),
        middlewares=[result_middleware],
        modules={"module": (ModuleForTest,)})
    return w3


def test_result_formatter(dummy_w3):
    assert dummy_w3.module.method() == 'OKAY'
