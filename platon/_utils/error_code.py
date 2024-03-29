RestrictingMaxEpochSize = 36
ERROR_CODE = {
    # successful
    0: 'sendRawTransaction successful',
    # System error
    1: 'System error',
    # Object not found
    2: 'Object not found',
    # Invalid parameter
    3: 'Invalid parameter',
    # restricting error code
    304001: 'The initial epoch for staking cannot be zero',
    304002: 'The number of the restricting plan cannot be (0, {}]'.format(RestrictingMaxEpochSize),
    304003: 'Total staking amount shall be more than 1 LAT',
    304004: 'Create plan,the sender balance is not enough in restrict',
    304005: 'Account is not found on restricting contract',
    304006: 'Slashing amount is larger than staking amount',
    304007: 'Staking amount cannot be 0',
    304008: 'Pledge lock funds amount cannot be less than or equal to 0',
    304009: 'Return lock funds amount cannot be less than or equal to 0',
    304010: 'Slashing amount cannot be less than 0',
    304011: 'Create plan each amount cannot be less than or equal to 0',
    304012: 'The staking amount is less than the return amount',
    304013: 'The user restricting balance is not enough for pledge lock funds',
    304014: 'Create plan each amount should greater than mini amount',
    304015: 'The user restricting  and free balance is not enough for pledge lock funds',
    # staking and delegate error code
    301000: 'Invalid BLS public key length',
    301001: 'The BLS proof is incorrect',
    301002: 'The Description length is incorrect',
    301003: 'The program version signature is invalid',
    301004: 'The program version is too low',
    301005: 'The Version Declaration is failed when creating staking',
    301006: 'The address must be the same as the one initiated staking',
    301007: 'Invalid param RewardPer',
    301008: 'Modify the commission reward ratio too frequently',
    301009: 'The modification range exceeds the limit',
    301100: 'Staking deposit is insufficient',
    301101: 'The candidate already existed',
    301102: 'The candidate does not exist',
    301103: 'This candidate status is expired',
    301104: 'Increased stake is insufficient',
    301105: 'Delegate deposit is insufficient',
    301106: 'The account is not allowed to delegate',
    301107: 'The candidate is not allowed to delegate',
    301108: 'Withdrawal of delegation is insufficient',
    301109: 'The delegate does not exist',
    301110: 'The von operation type is incorrect',
    301111: 'The account balance is insufficient',
    301112: 'The blockNumber is inconsistent with the expected number',
    301113: 'The balance of delegate is insufficient',
    301114: 'The amount of delegate withdrawal is incorrect',
    301115: 'The validator does not exist',
    301116: 'The fn params is invalid',
    301117: 'The slash type is illegal',
    301118: 'The amount of slash is overflowed',
    301119: 'The amount of slash for decreasing staking is incorrect',
    301200: 'Retreiving verifier list failed',
    301201: 'Retreiving validator list failed',
    301202: 'Retreiving candidate list failed',
    301203: 'Retreiving delegation related mapping failed',
    301204: 'Query candidate info failed',
    301205: 'Query delegate info failed',
    301206: 'Failed to convert Node ID to address',
    301207: 'The user delegation lock balance is not enough for delegate',
    301208: 'Query delegation lock info failed',
    305001: 'Delegation info not found',
    # slashing error code
    303000: 'Double-signning verification failed',
    303001: 'Punishment has been executed already',
    303002: 'BlockNumber for the reported double-spending attack is higher than the current value',
    303003: 'Reported evidence expired',
    303004: 'Failed to retrieve the reported validator information',
    303005: 'The evidence address is inconsistent with the validator address',
    303006: 'NodeId does not match',
    303007: 'BlsPubKey does not match',
    303008: 'Slashing node failed',
    303009: 'This node is not a validator',
    303010: "Can't report yourself",
    # pip error code
    302001: 'Current active version not found',
    302002: 'Illegal voting option',
    302003: 'Illegal proposal type',
    302004: 'Proposal ID is null',
    302005: 'Proposal ID already existed',
    302006: 'Proposal not found',
    302007: 'PIPID is null',
    302008: 'PIPID already existed',
    302009: 'EndVotingRounds is too small',
    302010: 'EndVotingRounds is too large',
    302011: 'NewVersion should larger than current active version',
    302012: 'Another version proposal already existed at voting stage',
    302013: 'Another version proposal already existed at pre-active stage',
    302014: 'Another cancel proposal already existed at voting stage',
    302015: 'The proposal to be canceled is not found',
    302016: 'The proposal to be canceled proposal has an illegal version type',
    302017: 'The proposal to be canceled is not at voting stage',
    302018: 'The proposer is null',
    302019: 'Detailed verifier information is not found',
    302020: 'The verifier status is invalid',
    302021: 'Transaction account is inconsistent with the staking account',
    302022: 'Transaction node is not the validator',
    302023: 'Transaction node is not the candidate',
    302024: 'Invalid version signature',
    302025: 'Verifier does not upgraded to the latest version',
    302026: 'The proposal is not at voting stage',
    302027: 'Duplicated votes found',
    302028: 'Declared version is invalid',
    302029: 'Error is found when notifying staking for the declared version',
    302030: 'The result of proposal is not found',
    302031: 'Unsupported governent parameter',
    302032: 'Another parameter proposal already existed at voting stage',
    302033: 'Govern parameter value error',
    302034: 'The new value of the parameter proposal is the same as the old one',
}
