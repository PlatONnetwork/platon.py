import pytest

from platon import Web3
from platon._utils.module import (
    attach_modules,
)
from platon.exceptions import (
    ValidationError,
)
from platon.module import (
    Module,
)
from platon.providers.platon_tester import (
    PlatonTesterProvider,
)


class MockPlaton(Module):
    def block_number(self):
        return 42


class MockGplaton(Module):
    pass


class MockGplatonAdmin(Module):
    def start_ws(self):
        return True


class MockGplatonPersonal(Module):
    def unlock_account(self):
        return True


def test_attach_modules():
    mods = {
        "gplaton": (MockGplaton, {
            "personal": (MockGplatonPersonal,),
            "admin": (MockGplatonAdmin,),
        }),
        "platon": (MockPlaton,),
    }
    w3 = Web3(PlatonTesterProvider(), modules={})
    attach_modules(w3, mods)
    assert w3.platon.block_number() == 42
    assert w3.gplaton.personal.unlock_account() is True
    assert w3.gplaton.admin.start_ws() is True


def test_attach_modules_multiple_levels_deep():
    mods = {
        "platon": (MockPlaton,),
        "gplaton": (MockGplaton, {
            "personal": (MockGplatonPersonal, {
                "admin": (MockGplatonAdmin,),
            }),
        }),
    }
    w3 = Web3(PlatonTesterProvider(), modules={})
    attach_modules(w3, mods)
    assert w3.platon.block_number() == 42
    assert w3.gplaton.personal.unlock_account() is True
    assert w3.gplaton.personal.admin.start_ws() is True


def test_attach_modules_with_wrong_module_format():
    mods = {
        "platon": (MockPlaton, MockGplaton, MockGplatonPersonal)
    }
    w3 = Web3(PlatonTesterProvider, modules={})
    with pytest.raises(ValidationError, match="Module definitions can only have 1 or 2 elements"):
        attach_modules(w3, mods)


def test_attach_modules_with_existing_modules():
    mods = {
        "platon": (MockPlaton,),
    }
    w3 = Web3(PlatonTesterProvider, modules=mods)
    with pytest.raises(AttributeError,
                       match="The platon object already has an attribute with that name"):
        attach_modules(w3, mods)
