from pydantic import BaseModel, Field
from typing import Any, List, Dict, Union, Optional


class ResponseModelBlockNumber(BaseModel):
    block_number: int


class ResponseModelDefaultAccount(BaseModel):
    default_account: Union[str, None]


class ResponseModelDefaultBlock(BaseModel):
    default_block: str


class ResponseModelMaxPriorityFee(BaseModel):
    max_priority_fee: int


class ResponseModelAccounts(BaseModel):
    accounts: list


class ResponseModelChainId(BaseModel):
    chain_id: Union[int, None]


class ResponseModelBalance(BaseModel):
    balance: int


class ResponseModelStorageAt(BaseModel):
    storage_value: str


class ResponseModelCode(BaseModel):
    bytecode: str


class ResponseModelTransactionCount(BaseModel):
    transaction_count: int


class ResponseModelEstimateGas(BaseModel):
    # TODO: not implemented because Enpoint is not working
    pass


class ErrorResponseModel(BaseModel):
    status_code: int
    detail: str
