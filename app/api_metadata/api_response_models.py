from pydantic import BaseModel
from typing import Union


class ExecutionClientGetBalanceResponseModel(BaseModel):
    balance: int


class ExecutionClientGetStorageAtResponseModel(BaseModel):
    storage_value: str