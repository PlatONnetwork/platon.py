from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    List,
    NewType,
    Optional,
    Sequence,
    Type,
    TypeVar,
    Union,
)

from platon_typing import (
    Address,
    BlockNumber,
    Bech32Address,
    Hash32,
    HexStr,
)

from hexbytes import (
    HexBytes,
)

from platon._utils.compat import (
    Literal,
    TypedDict,
)
from platon._utils.function_identifiers import (
    FallbackFn,
    ReceiveFn,
)
from platon.datastructures import (
    NamedElementOnion,
)

if TYPE_CHECKING:
    from platon import Web3  # noqa: F401

TReturn = TypeVar("TReturn")
TParams = TypeVar("TParams")
TValue = TypeVar("TValue")

BlockParams = Literal["latest", "earliest", "pending"]
BlockIdentifier = Union[BlockParams, BlockNumber, Hash32, HexStr, HexBytes, int]
LatestBlockParam = Literal["latest"]

FunctionIdentifier = Union[str, Type[FallbackFn], Type[ReceiveFn]]

# bytes, hexbytes, or hexstr representing a 32 byte hash
_Hash32 = Union[Hash32, HexBytes, HexStr]
EnodeURI = NewType("EnodeURI", str)
ENS = NewType("ENS", str)
Nonce = NewType("Nonce", int)
RPCEndpoint = NewType("RPCEndpoint", str)
Timestamp = NewType("Timestamp", int)
Wei = NewType('Wei', int)
Formatters = Dict[RPCEndpoint, Callable[..., Any]]


# todo: move these to platon_typing once platon is type hinted
class ABIEventParams(TypedDict, total=False):
    indexed: bool
    name: str
    type: str


class ABIEvent(TypedDict, total=False):
    anonymous: bool
    inputs: Sequence["ABIEventParams"]
    name: str
    type: Literal["event"]


class ABIFunctionComponents(TypedDict, total=False):
    # better typed as Sequence['ABIFunctionComponents'], but recursion isnt possible yet
    # https://github.com/python/mypy/issues/731
    components: Sequence[Any]
    name: str
    type: str


class ABIFunctionParams(TypedDict, total=False):
    components: Sequence["ABIFunctionComponents"]
    name: str
    type: str


class ABIFunction(TypedDict, total=False):
    constant: bool
    inputs: Sequence["ABIFunctionParams"]
    name: str
    outputs: Sequence["ABIFunctionParams"]
    payable: bool
    stateMutability: Literal["pure", "view", "nonpayable", "payable"]
    type: Literal["function", "constructor", "fallback", "receive"]


ABIElement = Union[ABIFunction, ABIEvent]
ABI = Sequence[Union[ABIFunction, ABIEvent]]


class EventData(TypedDict):
    address: Bech32Address
    args: Dict[str, Any]
    blockHash: HexBytes
    blockNumber: int
    event: str
    logIndex: int
    transactionHash: HexBytes
    transactionIndex: int


class RPCError(TypedDict):
    code: int
    message: str
    data: Optional[str]


class RPCResponse(TypedDict, total=False):
    error: Union[RPCError, str]
    id: int
    jsonrpc: Literal["2.0"]
    result: Any


Middleware = Callable[[Callable[[RPCEndpoint, Any], RPCResponse], "Web3"], Any]
MiddlewareOnion = NamedElementOnion[str, Middleware]


class FormattersDict(TypedDict, total=False):
    error_formatters: Formatters
    request_formatters: Formatters
    result_formatters: Formatters


class FilterParams(TypedDict, total=False):
    address: Union[Address, Bech32Address, List[Address], List[Bech32Address]]
    blockHash: HexBytes
    fromBlock: BlockIdentifier
    toBlock: BlockIdentifier
    topics: Sequence[Optional[Union[_Hash32, Sequence[_Hash32]]]]


class LogReceipt(TypedDict):
    address: Bech32Address
    blockHash: HexBytes
    blockNumber: BlockNumber
    data: HexStr
    logIndex: int
    payload: HexBytes
    removed: bool
    topic: HexBytes
    topics: Sequence[HexBytes]
    transactionHash: HexBytes
    transactionIndex: int


# syntax b/c "from" keyword not allowed w/ class construction
TxData = TypedDict("TxData", {
    "blockHash": HexBytes,
    "blockNumber": BlockNumber,
    "chain_id": int,
    "data": Union[bytes, HexStr],
    "from": Bech32Address,
    "gas": Wei,
    "gasPrice": Wei,
    "maxFeePerGas": Wei,
    "maxPriorityFeePerGas": Wei,
    "hash": HexBytes,
    "input": HexStr,
    "nonce": Nonce,
    "r": HexBytes,
    "s": HexBytes,
    "to": Bech32Address,
    "transactionIndex": int,
    "v": int,
    "value": Wei,
}, total=False)

# syntax b/c "from" keyword not allowed w/ class construction
TxParams = TypedDict("TxParams", {
    "chain_id": int,
    "data": Union[bytes, HexStr],
    # addr or ens
    "from": Union[Address, Bech32Address, str],
    "gas": Wei,
    # legacy pricing
    "gasPrice": Wei,
    # 1559 pricing
    "maxFeePerGas": Union[str, Wei],
    "maxPriorityFeePerGas": Union[str, Wei],
    "nonce": Nonce,
    # addr or ens
    "to": Union[Address, Bech32Address, str],
    "value": Wei,
}, total=False)


class CallOverrideParams(TypedDict):
    balance: Optional[Wei]
    nonce: Optional[int]
    code: Optional[Union[bytes, HexStr]]
    state: Optional[Dict[str, Any]]
    stateDiff: Optional[Dict[Address, Dict[str, Any]]]


GasPriceStrategy = Callable[["Web3", TxParams], Wei]

# syntax b/c "from" keyword not allowed w/ class construction
TxReceipt = TypedDict("TxReceipt", {
    "blockHash": HexBytes,
    "blockNumber": BlockNumber,
    "contractAddress": Optional[Bech32Address],
    "cumulativeGasUsed": int,
    "gasUsed": Wei,
    "from": Bech32Address,
    "logs": List[LogReceipt],
    "logsBloom": HexBytes,
    "root": HexStr,
    "status": int,
    "to": Bech32Address,
    "transactionHash": HexBytes,
    "transactionIndex": int,
})


class SignedTx(TypedDict, total=False):
    raw: bytes
    tx: TxParams


class StorageProof(TypedDict):
    key: HexStr
    proof: Sequence[HexStr]
    value: HexBytes


class MerkleProof(TypedDict):
    address: Bech32Address
    accountProof: Sequence[HexStr]
    balance: int
    codeHash: HexBytes
    nonce: Nonce
    storageHash: HexBytes
    storageProof: Sequence[StorageProof]


class Protocol(TypedDict):
    difficulty: int
    head: HexStr
    network: int
    version: int


class NodeInfo(TypedDict):
    enode: EnodeURI
    id: HexStr
    ip: str
    listenAddr: str
    name: str
    ports: Dict[str, int]
    protocols: Dict[str, Protocol]


class Peer(TypedDict, total=False):
    caps: Sequence[str]
    id: HexStr
    name: str
    network: Dict[str, str]
    protocols: Dict[str, Protocol]


class SyncStatus(TypedDict):
    currentBlock: int
    highestBlock: int
    knownStates: int
    pulledStates: int
    startingBlock: int


# todo: noqa
class BlockData(TypedDict, total=False):
    baseFeePerGas: Wei
    difficulty: int
    extraData: HexBytes
    gasLimit: Wei
    gasUsed: Wei
    hash: HexBytes
    logsBloom: HexBytes
    miner: Bech32Address
    mixHash: HexBytes
    nonce: HexBytes
    number: BlockNumber
    parentHash: HexBytes
    receiptRoot: HexBytes
    sha3Uncles: HexBytes
    size: int
    stateRoot: HexBytes
    timestamp: Timestamp
    totalDifficulty: int
    # list of tx hashes or of txdatas
    transactions: Union[Sequence[HexBytes], Sequence[TxData]]
    transactionsRoot: HexBytes


#
# txpool types
#

# syntax b/c "from" keyword not allowed w/ class construction
PendingTx = TypedDict("PendingTx", {
    "blockHash": HexBytes,
    "blockNumber": None,
    "from": Bech32Address,
    "gas": HexBytes,
    'maxFeePerGas': HexBytes,
    'maxPriorityFeePerGas': HexBytes,
    "gasPrice": HexBytes,
    "hash": HexBytes,
    "input": HexBytes,
    "nonce": HexBytes,
    "to": Bech32Address,
    "transactionIndex": None,
    "value": HexBytes,
}, total=False)


class TxPoolContent(TypedDict, total=False):
    pending: Dict[Bech32Address, Dict[Nonce, List[PendingTx]]]
    queued: Dict[Bech32Address, Dict[Nonce, List[PendingTx]]]


class TxPoolInspect(TypedDict, total=False):
    pending: Dict[Bech32Address, Dict[Nonce, str]]
    queued: Dict[Bech32Address, Dict[Nonce, str]]


class TxPoolStatus(TypedDict, total=False):
    pending: int
    queued: int


#
# platon.gplaton types
#


class GplatonWallet(TypedDict):
    accounts: Sequence[Dict[str, str]]
    status: str
    url: str


#
# platon.parity types
#

ParityBlockTrace = NewType("ParityBlockTrace", Dict[str, Any])
ParityFilterTrace = NewType("ParityFilterTrace", Dict[str, Any])
ParityMode = Literal["active", "passive", "dark", "offline"]
ParityTraceMode = Sequence[Literal["trace", "vmTrace", "stateDiff"]]


class ParityNetPeers(TypedDict):
    active: int
    connected: int
    max: int
    peers: List[Dict[Any, Any]]


class ParityFilterParams(TypedDict, total=False):
    after: int
    count: int
    fromAddress: Sequence[Union[Address, Bech32Address, ENS]]
    fromBlock: BlockIdentifier
    toAddress: Sequence[Union[Address, Bech32Address, ENS]]
    toBlock: BlockIdentifier
