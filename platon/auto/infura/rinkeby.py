from platon import Web3
from platon.middleware import (
    gplaton_poa_middleware,
)
from platon.providers.auto import (
    load_provider_from_uri,
)

from .endpoints import (
    INFURA_RINKEBY_DOMAIN,
    build_http_headers,
    build_infura_url,
)

_headers = build_http_headers()
_infura_url = build_infura_url(INFURA_RINKEBY_DOMAIN)

w3 = Web3(load_provider_from_uri(_infura_url, _headers))
w3.middleware_onion.inject(gplaton_poa_middleware, layer=0)
