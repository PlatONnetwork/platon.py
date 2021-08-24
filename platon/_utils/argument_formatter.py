from platon.types import InnerFn
from platon._utils.normalizers import abi_bytes_to_bytes, abi_address_to_bytes

INNER_CONTRACT_NORMALIZERS = [
    abi_bytes_to_bytes,
    abi_address_to_bytes,
]

INNER_CONTRACT_DEFAULT_ABIS = {
    'node_id': 'bytes',
}

CREATE_STAKING_ABIS = {
    'benifit_address': 'address',
    'node_id': 'bytes',
    'version_sign': 'bytes',
    'bls_pubkey': 'bytes',
    'bls_proof': 'bytes',
}

EDIT_CANDIDATE_ABIS = {
    'benifit_address': 'address',
    'node_id': 'bytes',
}

GET_DELEGATE_LIST_ABIS = {
    'delegate_address': 'address',
}

GET_DELEGATE_INFO_ABIS = {
    'delegate_address': 'address',
}

INNER_CONTRACT_ABIS = {
    InnerFn.staking_createStaking: CREATE_STAKING_ABIS,
    InnerFn.staking_editCandidate: EDIT_CANDIDATE_ABIS,
    InnerFn.delegate_getDelegateList: GET_DELEGATE_LIST_ABIS,

}
