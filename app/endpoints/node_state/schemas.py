from pydantic import BaseModel, Field
from typing import Any, List, Dict, Union, Optional


class ResponseModelSyncingTrue(BaseModel):
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


class ResponseModelSyncingFalse(BaseModel):
    syncing: bool


class ResponseModelMining(BaseModel):
    mining: bool


class ResponseModelHashrate(BaseModel):
    hashrate: int


class ResponseModelApiVersion(BaseModel):
    api_version: str


class ResponseModelClientVersion(BaseModel):
    client_version: str


class ResponseModelForkSchedule(BaseModel):
    class Data(BaseModel):
        previous_version: str
        current_version: str
        epoch: str

    data: List[Data]


class ResponseModelSpec(BaseModel):
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


class ResponseModelDepositContract(BaseModel):
    class Data(BaseModel):
        chain_id: str
        address: str

    data: Data


class ResponseModelNodeIdentity(BaseModel):
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


class ResponseModelPeers(BaseModel):
    class Data(BaseModel):
        peer_id: str
        enr: str
        last_seen_p2p_address: str
        state: str
        direction: str

    data: List[Data]


class ResponseModelPeer(BaseModel):
    class Data(BaseModel):
        peer_id: str
        enr: str
        last_seen_p2p_address: str
        state: str
        direction: str

    data: Data


class ResponseModelHealth(BaseModel):
    health: int


class ResponseModelVersion(BaseModel):
    class Data(BaseModel):
        version: str

    data: Data


class ResponseModelSyncing(BaseModel):
    class Data(BaseModel):
        head_slot: str
        sync_distance: str
        is_syncing: bool
        is_optimistic: bool
        el_offline: bool

    data: Data


class ErrorResponseModel(BaseModel):
    status_code: int
    detail: str
