from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import get_current_active_user
from .schemas import *
from .parameters import *
from typing import Union
from app.connectors import execution_client
from app.api_params.api_decorators import *

router = APIRouter(
    prefix="/mainnet/history",
    tags=["Mainnet History"],
    dependencies=[Depends(get_current_active_user)],
    responses={503: {"description": "Node not available"}}
)


@router.get("/uncle_count",
            responses={200: {"model": ResponseModelGetUncleCount}, 400: {"model": ErrorResponseModel}, 503: {"model": ErrorResponseModel}})
@connection_decorator
async def uncle_count(
        block_identifier: Union[int,
                                str] = BLOCK_IDENTIFIER_UNCLE_QUERY_PARAMETER):
    """
    Returns the (integer) number of uncles associated with the block specified by block_identifier.
    Delegates to eth_getUncleCountByBlockNumber if block_identifier is an integer or one of the predefined block parameters 'latest', 'earliest', 'pending', otherwise delegates to eth_getUncleCountByBlockHash.

    Throws BlockNotFound if the block is not found.
    """
    response = execution_client.get_uncle_count(block_identifier)

    if response is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Block not found (block_identifier: {block_identifier})"
        )

    return response


@router.get("/uncle_by_block",
            responses={200: {"model": ResponseModelGetUncleByBlock}, 400: {"model": ErrorResponseModel}, 503: {"model": ErrorResponseModel}})
@connection_decorator
async def uncle_by_block(
        block_identifier: Union[int,
                                str] = BLOCK_IDENTIFIER_UNCLE_QUERY_PARAMETER,
        uncle_index: int = UNCLE_INDEX_QUERY_PARAMETER):
    """
    Returns the uncle at the index specified by uncle_index from the block specified by block_identifier.
    Delegates to eth_getUncleByBlockNumberAndIndex if block_identifier is an integer or one of the predefined block parameters 'latest', 'earliest', 'pending', otherwise delegates to eth_getUncleByBlockHashAndIndex.

    Throws BlockNotFound if the block is not found.
    """
    response = execution_client.get_uncle_by_block(
        block_identifier, uncle_index)

    if response is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Block not found (block_identifier: {block_identifier}, uncle_index: {uncle_index})"
        )

    return response


@router.get("/block",
            responses={200: {"model": Union[ResponseModelGetBlockFalse, ResponseModelGetBlockTrue]}, 400: {"model": ErrorResponseModel}, 503: {"model": ErrorResponseModel}})
@connection_decorator
async def block(
        block_identifier: Union[int, str,
                                None] = BLOCK_IDENTIFIER_OPTIONAL_QUERY_PARAMETER,
        full_transactions: bool = FULL_TRANSACTION_QUERY_PARAMETER):
    """
    Returns the block specified by block_identifier.
    Delegates to eth_getBlockByNumber if block_identifier is an integer or one of the predefined block parameters 'latest', 'earliest', 'pending', 'safe', 'finalized' - otherwise delegates to eth_getBlockByHash.

    Throws BlockNotFound error if the block is not found.

    If full_transactions is True then the 'transactions' key will contain full transactions objects. Otherwise it will be an array of transaction hashes.
    """
    response = execution_client.get_block(block_identifier, full_transactions)

    if response is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Block not found (block_identifier: {block_identifier})"
        )

    return response


@router.get("/transaction",
            responses={200: {"model": ResponseModelGetTransaction}, 400: {"model": ErrorResponseModel}, 503: {"model": ErrorResponseModel}})
@connection_decorator
async def transaction(
        transaction_hash: str = TRANSACTION_HASH_QUERY_PARAMETER):
    """
    Returns the transaction specified by transaction_hash. 

    Throws TransactionNotFound if a transaction is not found at specified arguments.
    """
    response = execution_client.get_transaction(transaction_hash)

    if response is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Transaction not found (transaction_hash: {transaction_hash})"
        )

    return response


@router.get("/transaction_by_block",
            responses={200: {"model": ResponseModelGetTransactionByBlock}, 400: {"model": ErrorResponseModel}, 503: {"model": ErrorResponseModel}})
@connection_decorator
async def transaction_by_block(
        block_identifier: Union[int, str] = BLOCK_IDENTIFIER_QUERY_PARAMETER,
        transaction_index: int = TRANSACTION_INDEX_QUERY_PARAMETER):
    """
    Returns the transaction at the index specified by transaction_index from the block specified by block_identifier.
    Delegates to eth_getTransactionByBlockNumberAndIndex if block_identifier is an integer or one of the predefined block parameters 'latest', 'earliest', 'pending', 'safe', 'finalized', otherwise delegates to eth_getTransactionByBlockHashAndIndex.

    Throws TransactionNotFound if a transaction is not found at specified arguments.
    """
    response = execution_client.get_transaction_by_block(
        block_identifier, transaction_index)

    if response is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Transaction not found (block_identifier: {block_identifier}, transaction_index: {transaction_index})"
        )

    return response


@router.get("/block_transaction_count",
            responses={200: {"model": ResponseModelGetBlockTransactionCount}, 400: {"model": ErrorResponseModel}, 503: {"model": ErrorResponseModel}})
@connection_decorator
async def block_transaction_count(
        block_identifier: Union[int, str] = BLOCK_IDENTIFIER_QUERY_PARAMETER):
    """
    Returns the number of transactions in the block specified by block_identifier.
    Delegates to eth_getBlockTransactionCountByNumber if block_identifier is an integer or one of the predefined block parameters 'latest', 'earliest', 'pending', 'safe', 'finalized', otherwise delegates to eth_getBlockTransactionCountByHash.

    Throws BlockNotFoundError if transactions are not found.
    """
    response = execution_client.get_block_transaction_count(block_identifier)

    if response is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Block not found (block_identifier: {block_identifier})"
        )

    return response


@router.get("/transaction_receipt",
            responses={200: {"model": ResponseModelGetTransactionReceipt}, 400: {"model": ErrorResponseModel}, 503: {"model": ErrorResponseModel}})
@connection_decorator
async def transaction_receipt(
        transaction_hash: str = TRANSACTION_HASH_QUERY_PARAMETER):
    """
    Returns the transaction receipt specified by transaction_hash.

    Throws TransactionNotFound if a transaction cannot be found.

    If status in response equals 1 the transaction was successful. If it is equals 0 the transaction was reverted by EVM.
    """
    response = execution_client.get_transaction_receipt(transaction_hash)

    if response is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Transaction not found (transaction_hash: {transaction_hash})"
        )

    return response
