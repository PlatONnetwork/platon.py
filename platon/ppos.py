from typing import TYPE_CHECKING

from platon.module import Module
from platon._utils.staking import Staking
from platon._utils.delegate import Delegate
from platon._utils.slashing import Slashing

if TYPE_CHECKING:
    pass


class Ppos(Module):
    staking: Staking
    delegate: Delegate
    slashing: Slashing
