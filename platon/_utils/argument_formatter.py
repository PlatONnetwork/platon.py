from platon.types import (
    InnerFn,
)
from platon._utils.normalizers import (
    abi_bytes_to_bytes,
    abi_address_to_bytes,
)


INNER_CONTRACT_NORMALIZERS = [
    abi_bytes_to_bytes,
    abi_address_to_bytes,
]

DEFAULT_PARAM_ABIS = {
    'address': 'address',
    'node_id': 'bytes',
    'proposal_id': 'bytes',
}

CREATE_STAKING_ABIS = {
    'benefit_address': 'address',
    'node_id': 'bytes',
    'version_sign': 'bytes',
    'bls_pubkey': 'bytes',
    'bls_proof': 'bytes',
}

EDIT_CANDIDATE_ABIS = {
    'benefit_address': 'address',
    'node_id': 'bytes',
}

GET_DELEGATE_LIST_ABIS = {
    'delegate_address': 'address',
}

GET_DELEGATE_INFO_ABIS = {
    'delegate_address': 'address',
}

VOTE_ABIS = {
    'version_sign': 'bytes',
}

DECLARE_VERSION_ABIS = {
    'version_sign': 'bytes',
}

CREATE_RESTRICTING_ABIS = {
    'release_address': 'address',
}

GET_RESTRICTING_INFO_ABIS = {
    'release_address': 'address',
}


INNER_CONTRACT_ABIS = {
    # staking
    InnerFn.staking_createStaking: CREATE_STAKING_ABIS,
    InnerFn.staking_editStaking: EDIT_CANDIDATE_ABIS,
    InnerFn.delegate_getDelegateList: GET_DELEGATE_LIST_ABIS,
    InnerFn.delegate_getDelegateInfo: GET_DELEGATE_INFO_ABIS,
    # govern
    InnerFn.govern_vote: VOTE_ABIS,
    InnerFn.govern_declareVersion: DECLARE_VERSION_ABIS,

}
