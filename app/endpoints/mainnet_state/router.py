from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import get_current_active_user
from .schemas import *
from .parameters import *
from app.connectors import execution_client

router = APIRouter(
    prefix="/mainnet/state",
    tags=["Mainnet State"],
    dependencies=[Depends(get_current_active_user)]
)


@router.get("/block_number", response_model=ResponseModelBlockNumber)
async def block_number():
    """
    Returns the number of most recent block.
    """
    response = execution_client.block_number()
    return response


@router.get("/default_account", response_model=ResponseModelDefaultAccount)
async def default_account():
    """
    Returns the ethereum address that will be used as the default from address for all transactions.

    Defaults to empty.
    """
    response = execution_client.default_account()
    return response


@router.get("/default_block", response_model=ResponseModelDefaultBlock)
async def default_block():
    """
    Returns the default block number that will be used for any RPC methods that accept a block identifier.

    Defaults to 'latest'.
    """
    response = execution_client.default_block()
    return response


@router.get("/max_priority_fee", response_model=ResponseModelMaxPriorityFee)
async def max_priority_fee():
    """
    Returns a suggestion for a max priority fee for dynamic fee transactions in Wei.
    """
    response = execution_client.max_priority_fee()
    return response


@router.get("/accounts", response_model=ResponseModelAccounts)
async def accounts():
    """
    Returns the list of known accounts.
    """
    response = execution_client.accounts()
    return response


@router.get("/chain_id", response_model=ResponseModelChainId)
async def chain_id():
    """
    Returns an integer value for the currently configured “Chain Id” value introduced in EIP-155.

    Returns None if no Chain Id is available.
    """
    response = execution_client.chain_id()

    return response


@router.get("/balance", response_model=ResponseModelBalance)
async def balance(
        wallet_address: str = WALLET_ADDRESS_QUERY_PARAMETER,
        block_identifier: Union[int, str,
                                None] = BLOCK_IDENTIFIER_OPTIONAL_QUERY_PARAMETER,
):
    """
    Returns the balance of the given wallet_address at the block specified by block_identifier.

    wallet_address may be a checksum address or an ENS name
    """
    response = execution_client.get_balance(wallet_address, block_identifier)
    return response


@router.get("/storage_at", response_model=ResponseModelStorageAt)
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
    response = execution_client.get_storage_at(
        wallet_address, position, block_identifier)
    return response


@router.get("/code", response_model=ResponseModelCode)
async def code(
        wallet_address: str = WALLET_ADDRESS_QUERY_PARAMETER,
):
    """
    Returns the bytecode for the given wallet_address at the block specified by block_identifier.

    wallet_address may be a checksum address or an ENS name
    """
    response = execution_client.get_code(wallet_address)
    return response


@router.get("/transaction_count", response_model=ResponseModelTransactionCount)
async def transaction_count(
        wallet_address: str = WALLET_ADDRESS_QUERY_PARAMETER,
        block_identifier: Union[int, str,
                                None] = BLOCK_IDENTIFIER_OPTIONAL_QUERY_PARAMETER,
):
    """
    Returns the number of transactions that have been sent from wallet_address as of the block specified by block_identifier.

    wallet_address may be a checksum address or an ENS name
    """
    reponse = execution_client.get_transaction_count(
        wallet_address, block_identifier)
    return reponse


@router.get("/estimate_gas", response_model=ResponseModelEstimateGas)
async def estimate_gas(
        from_address: str = FROM_ADDRESS_QUERY_PARAMETER,
        to_address: str = TO_ADDRESS_QUERY_PARAMETER,
        value: int = TRANSACTION_VALUE_QUERY_PARAMETER,
):
    """
    Executes the given transaction locally without creating a new transaction on the blockchain. Returns amount of gas consumed by execution which can be used as a gas estimate.

    The transaction and block_identifier parameters are handled in the same manner as the send_transaction() method.
    """
    # TODO: not working -> node not fully synced
    response = execution_client.estimate_gas(from_address, to_address, value)
    return response