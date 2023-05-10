from pydantic import BaseModel, Field
from typing import Any, List, Dict, Union, Optional


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
    input_decoded: Optional[Dict] = None
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


class ResponseModelGetBlockTransactionCount(BaseModel):
    block_transaction_count: int


class ResponseModelGetUncleCount(BaseModel):
    uncle_count: int


class ResponseModelGetBlockFalse(BaseModel):
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


class ResponseModelGetBlockTrue(BaseModel):
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


class ResponseModelGetTransactionByBlock(Transaction):
    pass


class ResponseModelGetTransaction(Transaction):
    pass


class ResponseModelGetTransactionReceipt(BaseModel):
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


class ResponseModelGetUncleByBlock(BaseModel):
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


class ErrorResponseModel(BaseModel):
    status_code: int
    detail: str
