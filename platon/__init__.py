import sys
import warnings

import pkg_resources

from platon_account import (
    Account  # noqa: E402,
)
from platon.main import (
    Web3  # noqa: E402,
)
from platon.providers.platon_tester import (  # noqa: E402
    PlatonTesterProvider,
)
from platon.providers.ipc import (  # noqa: E402
    IPCProvider,
)
from platon.providers.rpc import (  # noqa: E402
    HTTPProvider,
)
from platon.providers.async_rpc import (  # noqa: E402
    AsyncHTTPProvider,
)
from platon.providers.websocket import (  # noqa: E402
    WebsocketProvider,
)

if (3, 5) <= sys.version_info < (3, 6):
    warnings.warn(
        "Support for Python 3.5 will be removed in platon.py v5",
        category=DeprecationWarning,
        stacklevel=2)

if sys.version_info < (3, 5):
    raise EnvironmentError(
        "Python 3.5 or above is required. "
        "Note that support for Python 3.5 will be removed in platon.py v5")


__version__ = pkg_resources.get_distribution("platon.py").version

__all__ = [
    "__version__",
    "Web3",
    "HTTPProvider",
    "IPCProvider",
    "WebsocketProvider",
    "TestRPCProvider",
    "PlatonTesterProvider",
    "Account",
    "AsyncHTTPProvider",
]
