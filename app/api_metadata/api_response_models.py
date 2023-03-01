from pydantic import BaseModel, Field
from typing import Any, List, Dict, Union, Optional


# Additional Models

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


# Execution Client Gossip Methods

class ExecutionClientResponseModelBlockNumber(BaseModel):
    block_number: int


# Execution Client State Methods

class ExecutionClientResponseModelDefaultAccount(BaseModel):
    default_account: Union[str, None]


class ExecutionClientResponseModelDefaultBlock(BaseModel):
    default_block: str


class ExecutionClientResponseModelSyncing(BaseModel):
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


class ExecutionClientResponseModelMining(BaseModel):
    mining: bool


class ExecutionClientResponseModelHashrate(BaseModel):
    hashrate: int


class ExecutionClientResponseModelMaxPriorityFee(BaseModel):
    max_priority_fee: int


class ExecutionClientResponseModelAccounts(BaseModel):
    accounts: list


class ExecutionClientResponseModelChainId(BaseModel):
    chain_id: int


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


class ExecutionClientResponseModelGetTransactionReceipt(BaseModel):
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
    block_number: int


class ConsensusClientResponseModelGetHashRoot(BaseModel):
    block_number: int


class ConsensusClientResponseModelGetForkData(BaseModel):
    block_number: int


class ConsensusClientResponseModelGetFinalityCheckpoint(BaseModel):
    block_number: int


class ConsensusClientResponseModelGetValidators(BaseModel):
    block_number: int


class ConsensusClientResponseModelGetValidator(BaseModel):
    block_number: int


class ConsensusClientResponseModelGetValidatorBalances(BaseModel):
    block_number: int


class ConsensusClientResponseModelGetEpochCommittees(BaseModel):
    block_number: int


class ConsensusClientResponseModelGetBlockHeaders(BaseModel):
    block_number: int


class ConsensusClientResponseModelGetBlockHeader(BaseModel):
    block_number: int


class ConsensusClientResponseModelGetBlock(BaseModel):
    block_number: int


class ConsensusClientResponseModelGetBlockRoot(BaseModel):
    block_number: int


class ConsensusClientResponseModelGetBlockAttestations(BaseModel):
    block_number: int


class ConsensusClientResponseModelGetAttestations(BaseModel):
    block_number: int


class ConsensusClientResponseModelGetAttesterSlashings(BaseModel):
    block_number: int


class ConsensusClientResponseModelGetProposerSlashings(BaseModel):
    block_number: int


class ConsensusClientResponseModelGetVoluntaryExists(BaseModel):
    block_number: int


# Consensus Client Config Methods

class ConsensusClientResponseModelGetForkSchedule(BaseModel):
    block_number: int


class ConsensusClientResponseModelGetSpec(BaseModel):
    block_number: int


class ConsensusClientResponseModelGetDepositContract(BaseModel):
    block_number: int


# Consensus Client Node Methods

class ConsensusClientResponseModelGetNodeIdentity(BaseModel):
    block_number: int


class ConsensusClientResponseModelGetPeers(BaseModel):
    block_number: int


class ConsensusClientResponseModelGetPeer(BaseModel):
    block_number: int


class ConsensusClientResponseModelGetHealth(BaseModel):
    block_number: int


class ConsensusClientResponseModelGetVersion(BaseModel):
    block_number: int


class ConsensusClientResponseModelGetSyncing(BaseModel):
    block_number: int
