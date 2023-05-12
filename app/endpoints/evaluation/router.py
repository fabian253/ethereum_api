from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import get_current_active_user
from .schemas import *
from .parameters import *
from .utils import *
from typing import Union
from app.connectors import execution_client
from app.api_params.api_decorators import *

router = APIRouter(
    prefix="/evaluation",
    tags=["Evaluation"],
    dependencies=[Depends(get_current_active_user)]
)


@router.get("/evaluate_block_request_time", responses={503: {"model": ErrorResponseModel}})
@connection_decorator
async def evaluate_block_request_time(
        block_identifier_list: list[Union[int, str]
                                    ] = BLOCK_IDENTIFIER_LIST_QUERY_PARAMETER,
        full_transactions: bool = FULL_TRANSACTION_QUERY_PARAMETER):
    """
    Evaluate request time of get_block method.

    If full_transactions is True then the 'transactions' key will contain full transactions objects. Otherwise it will be an array of transaction hashes.
    """
    response = evaluate_request_time_get_block(
        execution_client, block_identifier_list, full_transactions)

    return response


@router.get("/evaluate_transaction_request_time", responses={503: {"model": ErrorResponseModel}})
@connection_decorator
async def evaluate_block_request_time(
        transaction_hash_list: list[str] = TRANSACTION_HASH_LIST_QUERY_PARAMETER):
    """
    Evaluate request time of get_transaction method.

    If full_transactions is True then the 'transactions' key will contain full transactions objects. Otherwise it will be an array of transaction hashes.
    """
    response = evaluate_request_time_get_transaction(
        execution_client, transaction_hash_list)

    return response
