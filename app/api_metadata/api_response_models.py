from pydantic import BaseModel, Field
from typing import Any, List, Union, Optional


# Execution Client Additional Models

class Transaction(BaseModel):
    blockHash: str
    blockNumber: int
    from_: str = Field(..., alias='from')
    gas: int
    gasPrice: int
    maxFeePerGas: Optional[int] = None
    maxPriorityFeePerGas: Optional[int] = None
    hash: str
    input: str
    nonce: int
    to: str
    transactionIndex: int
    value: int
    type: str
    accessList: Optional[List] = None
    chainId: Optional[str] = None
    v: int
    r: str
    s: str


# Execution Client Gossip Methods

class ExecutionClientResponseModelBlockNumber(BaseModel):
    block_number: int


# Execution Client State Methods

class ExecutionClientResponseModelDefaultAccount(BaseModel):
    default_account: Union[str, None]


class ExecutionClientResponseModelDefaultBlock(BaseModel):
    default_block: str


class ExecutionClientResponseModelSyncingTrue(BaseModel):
    currentBlock: int
    healedBytecodeBytes: str
    healedBytecodes: str
    healedTrienodeBytes: str
    healedTrienodes: str
    healingBytecode: str
    healingTrienodes: str
    highestBlock: int
    startingBlock: int
    syncedAccountBytes: str
    syncedAccounts: str
    syncedBytecodeBytes: str
    syncedBytecodes: str
    syncedStorage: str
    syncedStorageBytes: str


class ExecutionClientResponseModelSyncingFalse(BaseModel):
    syncing: bool


class ExecutionClientResponseModelMining(BaseModel):
    mining: bool


class ExecutionClientResponseModelHashrate(BaseModel):
    hashrate: int


class ExecutionClientResponseModelMaxPriorityFee(BaseModel):
    max_priority_fee: int


class ExecutionClientResponseModelAccounts(BaseModel):
    accounts: list


class ExecutionClientResponseModelChainId(BaseModel):
    chain_id: Union[int, None]


class ExecutionClientResponseModelGetApiVersion(BaseModel):
    api_version: str


class ExecutionClientResponseModelGetClientVersion(BaseModel):
    client_version: str


class ExecutionClientResponseModelGetBalance(BaseModel):
    balance: int


class ExecutionClientResponseModelGetBlockNumber(BaseModel):
    block_number: int


class ExecutionClientResponseModelGetStorageAt(BaseModel):
    storage_value: str


class ExecutionClientResponseModelGetCode(BaseModel):
    bytecode: str


class ExecutionClientResponseModelGetTransactionCount(BaseModel):
    transaction_count: int


class ExecutionClientResponseModelEstimateGas(BaseModel):
    # TODO: not implemented because Enpoint is not working
    pass


# Execution Client History Methods

class ExecutionClientResponseModelGetBlockTransactionCount(BaseModel):
    block_transaction_count: int


class ExecutionClientResponseModelGetUncleCount(BaseModel):
    uncle_count: int


class ExecutionClientResponseModelGetBlockFalse(BaseModel):
    baseFeePerGas: Optional[int]
    difficulty: int
    extraData: str
    gasLimit: int
    gasUsed: int
    hash: str
    logsBloom: str
    miner: str
    mixHash: str
    nonce: str
    number: int
    parentHash: str
    receiptsRoot: str
    sha3Uncles: str
    size: int
    stateRoot: str
    timestamp: int
    totalDifficulty: float
    transactions: List[str]
    transactionsRoot: str
    uncles: List
    withdrawals: Any


class ExecutionClientResponseModelGetBlockTrue(BaseModel):
    baseFeePerGas: Optional[int]
    difficulty: int
    extraData: str
    gasLimit: int
    gasUsed: int
    hash: str
    logsBloom: str
    miner: str
    mixHash: str
    nonce: str
    number: int
    parentHash: str
    receiptsRoot: str
    sha3Uncles: str
    size: int
    stateRoot: str
    timestamp: int
    totalDifficulty: float
    transactions: List[Transaction]
    transactionsRoot: str
    uncles: List
    withdrawals: Any


class ExecutionClientResponseModelGetTransactionByBlock(Transaction):
    pass


class ExecutionClientResponseModelGetTransaction(Transaction):
    pass


class ExecutionClientResponseModelGetTransactionReceipt(BaseModel):
    class Log(BaseModel):
        address: str
        topics: List[str]
        data: str
        blockNumber: int
        transactionHash: str
        transactionIndex: int
        blockHash: str
        logIndex: int
        removed: bool

    blockHash: str
    blockNumber: int
    contractAddress: Any
    cumulativeGasUsed: int
    effectiveGasPrice: int
    from_: str = Field(..., alias='from')
    gasUsed: int
    logs: List[Log]
    logsBloom: str
    status: int
    to: str
    transactionHash: str
    transactionIndex: int
    type: str


class ExecutionClientResponseModelGetUncleByBlock(BaseModel):
    difficulty: str
    extraData: str
    gasLimit: str
    gasUsed: str
    hash: str
    logsBloom: str
    miner: str
    mixHash: str
    nonce: str
    number: str
    parentHash: str
    receiptsRoot: str
    sha3Uncles: str
    size: str
    stateRoot: str
    timestamp: str
    transactionsRoot: str
    uncles: List


# Consensus Client Beacon Methods
# TODO: implement Models

class ConsensusClientResponseModelGetGenesis(BaseModel):
    class Data(BaseModel):
        genesis_time: str
        genesis_validators_root: str
        genesis_fork_version: str

    data: Data


class ConsensusClientResponseModelGetHashRoot(BaseModel):
    class Data(BaseModel):
        root: str

    data: Data
    execution_optimistic: bool
    finalized: bool


class ConsensusClientResponseModelGetForkData(BaseModel):
    class Data(BaseModel):
        previous_version: str
        current_version: str
        epoch: str

    data: Data
    execution_optimistic: bool
    finalized: bool


class ConsensusClientResponseModelGetFinalityCheckpoint(BaseModel):
    class Data(BaseModel):
        class PreviousJustified(BaseModel):
            epoch: str
            root: str

        class CurrentJustified(BaseModel):
            epoch: str
            root: str

        class Finalized(BaseModel):
            epoch: str
            root: str

        previous_justified: PreviousJustified
        current_justified: CurrentJustified
        finalized: Finalized

    data: Data
    execution_optimistic: bool
    finalized: bool


class ConsensusClientResponseModelGetValidators(BaseModel):
    # TODO: Endpoint not working
    class Data(BaseModel):
        class Validator(BaseModel):
            pubkey: str
            withdrawal_credentials: str
            effective_balance: str
            slashed: bool
            activation_eligibility_epoch: str
            activation_epoch: str
            exit_epoch: str
            withdrawable_epoch: str

        index: str
        balance: str
        status: str
        validator: Validator

    execution_optimistic: bool
    data: List[Data]


class ConsensusClientResponseModelGetValidator(BaseModel):
    class Data(BaseModel):
        class Validator(BaseModel):
            pubkey: str
            withdrawal_credentials: str
            effective_balance: str
            slashed: bool
            activation_eligibility_epoch: str
            activation_epoch: str
            exit_epoch: str
            withdrawable_epoch: str

        index: str
        balance: str
        status: str
        validator: Validator

    execution_optimistic: bool
    data: Data


class ConsensusClientResponseModelGetValidatorBalances(BaseModel):
    class Data(BaseModel):
        index: str
        balance: str

    execution_optimistic: bool
    data: List[Data]


class ConsensusClientResponseModelGetEpochCommittees(BaseModel):
    class Data(BaseModel):
        index: str
        slot: str
        validators: List[str]

    data: List[Data]
    execution_optimistic: bool
    finalized: bool


class ConsensusClientResponseModelGetBlockHeaders(BaseModel):
    class Data(BaseModel):
        class Header(BaseModel):
            class Message(BaseModel):
                slot: str
                proposer_index: str
                parent_root: str
                state_root: str
                body_root: str

            message: Message
            signature: str

        root: str
        canonical: bool
        header: Header

    data: List[Data]
    execution_optimistic: bool
    finalized: bool


class ConsensusClientResponseModelGetBlockHeader(BaseModel):
    class Data(BaseModel):
        class Header(BaseModel):
            class Message(BaseModel):
                slot: str
                proposer_index: str
                parent_root: str
                state_root: str
                body_root: str

            message: Message
            signature: str

        root: str
        canonical: bool
        header: Header

    data: Data
    execution_optimistic: bool
    finalized: bool


class ConsensusClientResponseModelGetBlock(BaseModel):
    class Data(BaseModel):
        class Message(BaseModel):
            class Body(BaseModel):
                class Eth1Data(BaseModel):
                    deposit_root: str
                    deposit_count: str
                    block_hash: str

                class Attestation(BaseModel):
                    class Data1(BaseModel):
                        class Source(BaseModel):
                            epoch: str
                            root: str

                        class Target(BaseModel):
                            epoch: str
                            root: str

                        slot: str
                        index: str
                        beacon_block_root: str
                        source: Source
                        target: Target

                    aggregation_bits: str
                    data: Data1
                    signature: str

                randao_reveal: str
                eth1_data: Eth1Data
                graffiti: str
                proposer_slashings: List
                attester_slashings: List
                attestations: List[Attestation]
                deposits: List
                voluntary_exits: List

            slot: str
            proposer_index: str
            parent_root: str
            state_root: str
            body: Body

        message: Message
        signature: str

    data: Data


class ConsensusClientResponseModelGetBlockRoot(BaseModel):
    class Data(BaseModel):
        root: str

    data: Data
    execution_optimistic: bool
    finalized: bool


class ConsensusClientResponseModelGetBlockAttestations(BaseModel):
    class Data(BaseModel):

        class Data(BaseModel):
            class Source(BaseModel):
                epoch: str
                root: str

            class Target(BaseModel):
                epoch: str
                root: str

            slot: str
            index: str
            beacon_block_root: str
            source: Source
            target: Target

        aggregation_bits: str
        data: Data
        signature: str

    data: List[Data]
    execution_optimistic: bool
    finalized: bool


class ConsensusClientResponseModelGetAttestations(BaseModel):
    class Data(BaseModel):
        class Data(BaseModel):
            class Source(BaseModel):
                epoch: str
                root: str

            class Target(BaseModel):
                epoch: str
                root: str

            slot: str
            index: str
            beacon_block_root: str
            source: Source
            target: Target

        aggregation_bits: str
        data: Data
        signature: str

    data: List[Data]


class ConsensusClientResponseModelGetAttesterSlashings(BaseModel):
    # TODO: method and endpoint not working
    class Data(BaseModel):
        pass

    data: List


class ConsensusClientResponseModelGetProposerSlashings(BaseModel):
    # TODO: method and endpoint not working
    class Data(BaseModel):
        pass

    data: List


class ConsensusClientResponseModelGetVoluntaryExists(BaseModel):
    # TODO: method and endpoint not working
    class Data(BaseModel):
        pass

    data: List


# Consensus Client Config Methods

class ConsensusClientResponseModelGetForkSchedule(BaseModel):
    class Data(BaseModel):
        previous_version: str
        current_version: str
        epoch: str

    data: List[Data]


class ConsensusClientResponseModelGetSpec(BaseModel):
    class Data(BaseModel):
        ALTAIR_FORK_EPOCH: str
        ALTAIR_FORK_VERSION: str
        BASE_REWARD_FACTOR: str
        BELLATRIX_FORK_EPOCH: str
        BELLATRIX_FORK_VERSION: str
        BLS_WITHDRAWAL_PREFIX: str
        CAPELLA_FORK_EPOCH: str
        CAPELLA_FORK_VERSION: str
        CHURN_LIMIT_QUOTIENT: str
        CONFIG_NAME: str
        DEPOSIT_CHAIN_ID: str
        DEPOSIT_CONTRACT_ADDRESS: str
        DEPOSIT_NETWORK_ID: str
        DOMAIN_AGGREGATE_AND_PROOF: str
        DOMAIN_APPLICATION_MASK: str
        DOMAIN_BEACON_ATTESTER: str
        DOMAIN_BEACON_PROPOSER: str
        DOMAIN_CONTRIBUTION_AND_PROOF: str
        DOMAIN_DEPOSIT: str
        DOMAIN_RANDAO: str
        DOMAIN_SELECTION_PROOF: str
        DOMAIN_SYNC_COMMITTEE: str
        DOMAIN_SYNC_COMMITTEE_SELECTION_PROOF: str
        DOMAIN_VOLUNTARY_EXIT: str
        EFFECTIVE_BALANCE_INCREMENT: str
        EJECTION_BALANCE: str
        EPOCHS_PER_ETH1_VOTING_PERIOD: str
        EPOCHS_PER_HISTORICAL_VECTOR: str
        EPOCHS_PER_RANDOM_SUBNET_SUBSCRIPTION: str
        EPOCHS_PER_SLASHINGS_VECTOR: str
        EPOCHS_PER_SYNC_COMMITTEE_PERIOD: str
        ETH1_ADDRESS_WITHDRAWAL_PREFIX: str
        ETH1_FOLLOW_DISTANCE: str
        GENESIS_DELAY: str
        GENESIS_FORK_VERSION: str
        HISTORICAL_ROOTS_LIMIT: str
        HYSTERESIS_DOWNWARD_MULTIPLIER: str
        HYSTERESIS_QUOTIENT: str
        HYSTERESIS_UPWARD_MULTIPLIER: str
        INACTIVITY_PENALTY_QUOTIENT: str
        INACTIVITY_PENALTY_QUOTIENT_ALTAIR: str
        INACTIVITY_PENALTY_QUOTIENT_BELLATRIX: str
        INACTIVITY_SCORE_BIAS: str
        INACTIVITY_SCORE_RECOVERY_RATE: str
        INTERVALS_PER_SLOT: str
        MAX_ATTESTATIONS: str
        MAX_ATTESTER_SLASHINGS: str
        MAX_BLS_TO_EXECUTION_CHANGES: str
        MAX_COMMITTEES_PER_SLOT: str
        MAX_DEPOSITS: str
        MAX_EFFECTIVE_BALANCE: str
        MAX_PROPOSER_SLASHINGS: str
        MAX_SEED_LOOKAHEAD: str
        MAX_VALIDATORS_PER_COMMITTEE: str
        MAX_VALIDATORS_PER_WITHDRAWALS_SWEEP: str
        MAX_VOLUNTARY_EXITS: str
        MAX_WITHDRAWALS_PER_PAYLOAD: str
        MIN_ATTESTATION_INCLUSION_DELAY: str
        MIN_DEPOSIT_AMOUNT: str
        MIN_EPOCHS_TO_INACTIVITY_PENALTY: str
        MIN_GENESIS_ACTIVE_VALIDATOR_COUNT: str
        MIN_GENESIS_TIME: str
        MIN_PER_EPOCH_CHURN_LIMIT: str
        MIN_SEED_LOOKAHEAD: str
        MIN_SLASHING_PENALTY_QUOTIENT: str
        MIN_SLASHING_PENALTY_QUOTIENT_ALTAIR: str
        MIN_SLASHING_PENALTY_QUOTIENT_BELLATRIX: str
        MIN_SYNC_COMMITTEE_PARTICIPANTS: str
        MIN_VALIDATOR_WITHDRAWABILITY_DELAY: str
        PRESET_BASE: str
        PROPORTIONAL_SLASHING_MULTIPLIER: str
        PROPORTIONAL_SLASHING_MULTIPLIER_ALTAIR: str
        PROPORTIONAL_SLASHING_MULTIPLIER_BELLATRIX: str
        PROPOSER_REWARD_QUOTIENT: str
        PROPOSER_SCORE_BOOST: str
        PROPOSER_WEIGHT: str
        RANDOM_SUBNETS_PER_VALIDATOR: str
        REORG_MAX_EPOCHS_SINCE_FINALIZATION: str
        REORG_WEIGHT_THRESHOLD: str
        SAFE_SLOTS_TO_IMPORT_OPTIMISTICALLY: str
        SAFE_SLOTS_TO_UPDATE_JUSTIFIED: str
        SECONDS_PER_ETH1_BLOCK: str
        SECONDS_PER_SLOT: str
        SHARD_COMMITTEE_PERIOD: str
        SHUFFLE_ROUND_COUNT: str
        SLOTS_PER_EPOCH: str
        SLOTS_PER_HISTORICAL_ROOT: str
        SYNC_COMMITTEE_SIZE: str
        SYNC_COMMITTEE_SUBNET_COUNT: str
        SYNC_REWARD_WEIGHT: str
        TARGET_AGGREGATORS_PER_COMMITTEE: str
        TARGET_AGGREGATORS_PER_SYNC_SUBCOMMITTEE: str
        TARGET_COMMITTEE_SIZE: str
        TERMINAL_BLOCK_HASH: str
        TERMINAL_BLOCK_HASH_ACTIVATION_EPOCH: str
        TERMINAL_TOTAL_DIFFICULTY: str
        TIMELY_HEAD_FLAG_INDEX: str
        TIMELY_HEAD_WEIGHT: str
        TIMELY_SOURCE_FLAG_INDEX: str
        TIMELY_SOURCE_WEIGHT: str
        TIMELY_TARGET_FLAG_INDEX: str
        TIMELY_TARGET_WEIGHT: str
        VALIDATOR_REGISTRY_LIMIT: str
        WEIGHT_DENOMINATOR: str
        WHISTLEBLOWER_REWARD_QUOTIENT: str

    data: Data


class ConsensusClientResponseModelGetDepositContract(BaseModel):
    class Data(BaseModel):
        chain_id: str
        address: str

    data: Data


# Consensus Client Node Methods

class ConsensusClientResponseModelGetNodeIdentity(BaseModel):
    class Data(BaseModel):
        class Metadata(BaseModel):
            seq_number: str
            attnets: str

        peer_id: str
        enr: str
        p2p_addresses: List[str]
        discovery_addresses: List[str]
        metadata: Metadata

    data: Data


class ConsensusClientResponseModelGetPeers(BaseModel):
    class Data(BaseModel):
        peer_id: str
        enr: str
        last_seen_p2p_address: str
        state: str
        direction: str

    data: List[Data]


class ConsensusClientResponseModelGetPeer(BaseModel):
    class Data(BaseModel):
        peer_id: str
        enr: str
        last_seen_p2p_address: str
        state: str
        direction: str

    data: Data


class ConsensusClientResponseModelGetHealth(BaseModel):
    health: int


class ConsensusClientResponseModelGetVersion(BaseModel):
    class Data(BaseModel):
        version: str

    data: Data


class ConsensusClientResponseModelGetSyncing(BaseModel):
    class Data(BaseModel):
        head_slot: str
        sync_distance: str
        is_syncing: bool
        is_optimistic: bool
        el_offline: bool

    data: Data


# Error Models

class ErrorResponseModel(BaseModel):
    status_code: int
    detail: str
