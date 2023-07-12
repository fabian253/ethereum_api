from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import get_current_active_user
from .schemas import *
from .parameters import *
from app.connectors import execution_client
from app.api_params.api_decorators import *

router = APIRouter(
    prefix="/mainnet/state",
    tags=["Mainnet State"],
    dependencies=[Depends(get_current_active_user)],
    responses={503: {"description": "Node not available"}}
)


@router.get("/block_number", responses={200: {"model": ResponseModelBlockNumber}, 503: {"model": ErrorResponseModel}})
@connection_decorator
async def block_number():
    """
    Returns the number of most recent block.
    """
    response = execution_client.block_number()
    return response


@router.get("/default_account", responses={200: {"model": ResponseModelDefaultAccount}, 503: {"model": ErrorResponseModel}})
@connection_decorator
async def default_account():
    """
    Returns the ethereum address that will be used as the default from address for all transactions.

    Defaults to empty.
    """
    response = execution_client.default_account()
    return response


@router.get("/default_block", responses={200: {"model": ResponseModelDefaultBlock}, 503: {"model": ErrorResponseModel}})
@connection_decorator
async def default_block():
    """
    Returns the default block number that will be used for any RPC methods that accept a block identifier.

    Defaults to 'latest'.
    """
    response = execution_client.default_block()
    return response


@router.get("/max_priority_fee", responses={200: {"model": ResponseModelMaxPriorityFee}, 503: {"model": ErrorResponseModel}})
@connection_decorator
async def max_priority_fee():
    """
    Returns a suggestion for a max priority fee for dynamic fee transactions in Wei.
    """
    response = execution_client.max_priority_fee()
    return response


@router.get("/accounts", responses={200: {"model": ResponseModelAccounts}, 503: {"model": ErrorResponseModel}})
@connection_decorator
async def accounts():
    """
    Returns the list of known accounts.
    """
    response = execution_client.accounts()
    return response


@router.get("/chain_id", responses={200: {"model": ResponseModelChainId}, 503: {"model": ErrorResponseModel}})
@connection_decorator
async def chain_id():
    """
    Returns an integer value for the currently configured “Chain Id” value introduced in EIP-155.

    Returns None if no Chain Id is available.
    """
    response = execution_client.chain_id()

    return response


@router.get("/balance", responses={200: {"model": ResponseModelBalance}, 503: {"model": ErrorResponseModel}})
@connection_decorator
async def balance(
        wallet_address: str = WALLET_ADDRESS_QUERY_PARAMETER,
        block_identifier: Union[int, str,
                                None] = BLOCK_IDENTIFIER_OPTIONAL_QUERY_PARAMETER,
):
    """
    Returns the balance of the given wallet_address at the block specified by block_identifier.

    wallet_address may be a checksum address or an ENS name
    """
    try:
        response = execution_client.get_balance(
            wallet_address, block_identifier)
        return response
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wallet Address format incorrect."
        )


@router.get("/storage_at", responses={200: {"model": ResponseModelStorageAt}, 503: {"model": ErrorResponseModel}})
@connection_decorator
async def storage_at(
        wallet_address: str = WALLET_ADDRESS_QUERY_PARAMETER,
        position: int = POSITION_QUERY_PARAMETER,
        block_identifier: Union[int, str,
                                None] = BLOCK_IDENTIFIER_OPTIONAL_QUERY_PARAMETER,
):
    """
    Returns the value from a storage position for the given wallet_address at the block specified by block_identifier.

    wallet_address may be a checksum address or an ENS name
    """
    try:
        response = execution_client.get_storage_at(
            wallet_address, position, block_identifier)
        return response
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wallet Address format incorrect."
        )


@router.get("/code", responses={200: {"model": ResponseModelCode}, 503: {"model": ErrorResponseModel}})
@connection_decorator
async def code(
        wallet_address: str = WALLET_ADDRESS_QUERY_PARAMETER,
):
    """
    Returns the bytecode for the given wallet_address at the block specified by block_identifier.

    wallet_address may be a checksum address or an ENS name
    """
    try:
        response = execution_client.get_code(wallet_address)
        return response
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wallet Address format incorrect."
        )


@router.get("/transaction_count", responses={200: {"model": ResponseModelTransactionCount}, 503: {"model": ErrorResponseModel}})
@connection_decorator
async def transaction_count(
        wallet_address: str = WALLET_ADDRESS_QUERY_PARAMETER,
        block_identifier: Union[int, str,
                                None] = BLOCK_IDENTIFIER_OPTIONAL_QUERY_PARAMETER,
):
    """
    Returns the number of transactions that have been sent from wallet_address as of the block specified by block_identifier.

    wallet_address may be a checksum address or an ENS name
    """
    try:
        reponse = execution_client.get_transaction_count(
            wallet_address, block_identifier)
        return reponse
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wallet Address format incorrect."
        )


@router.get("/estimate_gas", responses={200: {"model": ResponseModelEstimateGas}, 400: {"model": ErrorResponseModel}, 503: {"model": ErrorResponseModel}})
@connection_decorator
async def estimate_gas(
        from_address: str = FROM_ADDRESS_QUERY_PARAMETER,
        to_address: str = TO_ADDRESS_QUERY_PARAMETER,
        value: int = TRANSACTION_VALUE_QUERY_PARAMETER,
):
    """
    Executes the given transaction locally without creating a new transaction on the blockchain. Returns amount of gas consumed by execution which can be used as a gas estimate.

    The transaction and block_identifier parameters are handled in the same manner as the send_transaction() method.
    """
    try:
        response = execution_client.estimate_gas(
            from_address, to_address, value)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.args[0]["message"]
        )
    return response
