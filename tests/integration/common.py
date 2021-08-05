import pytest

from websockets.exceptions import (
    ConnectionClosed,
)

from platon import Web3


class MiscWebsocketTest:

    def test_websocket_max_size_error(self, web3, endpoint_uri):
        w3 = Web3(Web3.WebsocketProvider(
            endpoint_uri=endpoint_uri, websocket_kwargs={'max_size': 1})
        )
        with pytest.raises((OSError, ConnectionClosed)):
            w3.platon.get_block(0)
