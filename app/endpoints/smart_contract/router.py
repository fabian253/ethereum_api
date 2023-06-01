from fastapi import APIRouter, Depends, HTTPException, status
from web3.exceptions import BlockNotFound, TransactionNotFound, NoABIFound, ABIFunctionNotFound, ABIEventFunctionNotFound, InvalidAddress
import app.config as config
from app.dependencies import get_current_active_user
from .schemas import *
from .parameters import *
from typing import Union
from app.connectors import execution_client, infura_execution_client, sql_db_connector, TokenStandard
from app.api_params.api_decorators import *

router = APIRouter(
    prefix="/mainnet/contract",
    tags=["Smart Contract"],
    dependencies=[Depends(get_current_active_user)],
    responses={503: {"description": "Node not available"}}
)


@router.get("/token_standard_abi", responses={503: {"model": ErrorResponseModel}})
async def token_standard_abi(
        token_standard: TokenStandard = TOKEN_STANDARD_QUERY_PARAMETER):
    """
    Returns the Contract Application Binary Interface (ABI) of a token standard.

    There are multiple token standards provided:
    * ERC20
    * ERC20Metadata
    * ERC165
    * ERC721
    * ERC721Enumerable
    * ERC721Metadata
    * ERC777Token
    * ERC1155
    * ERC1155TokenReceiver
    """
    response = execution_client.get_token_standard_abi(token_standard)

    return response


@router.get("/abi", responses={503: {"model": ErrorResponseModel}})
@connection_decorator
async def contract_abi(
        contract_address: str = CONTRACT_ADDRESS_QUERY_PARAMETER):
    """
    Returns the Contract Application Binary Interface (ABI) of a verified smart contract.
    """
    # TODO: remove infura when syced
    try:
        response = infura_execution_client.get_contract_abi(contract_address)
        return response
    except NoABIFound:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Contract not found (contract_address: {contract_address})"
        )


@router.get("/implemented_token_standards", responses={503: {"model": ErrorResponseModel}})
@connection_decorator
async def contract_implemented_token_standards(
        contract_address: str = CONTRACT_ADDRESS_QUERY_PARAMETER):
    """
    Return if token standards are implemented by contract Application Binary Interface (ABI).
    """
    # TODO: remove infura when syced
    try:
        response = infura_execution_client.get_contract_implemented_token_standards(
            contract_address)
        return response
    except NoABIFound:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Contract not found (contract_address: {contract_address})"
        )


@router.get("/function_overview", responses={503: {"model": ErrorResponseModel}})
@connection_decorator
async def contract_function_overview(
        contract_address: str = CONTRACT_ADDRESS_QUERY_PARAMETER,
        as_abi: bool = AS_ABI_QUERY_PARAMETER):
    """
    Returns all contract functions.
    """
    # TODO: remove infura when syced
    try:
        response = infura_execution_client.get_all_contract_functions(
            contract_address, as_abi)
        return response
    except NoABIFound:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Contract not found (contract_address: {contract_address})"
        )


@router.get("/event_overview", responses={503: {"model": ErrorResponseModel}})
@connection_decorator
async def contract_event_overview(
        contract_address: str = CONTRACT_ADDRESS_QUERY_PARAMETER,
        as_abi: bool = AS_ABI_QUERY_PARAMETER):
    """
    Returns all contract events.
    """
    # TODO: remove infura when syced
    try:
        response = infura_execution_client.get_all_contract_events(
            contract_address, as_abi)
        return response
    except NoABIFound:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Contract not found (contract_address: {contract_address})"
        )


@router.get("/events", responses={503: {"model": ErrorResponseModel}})
@connection_decorator
async def contract_events(
        contract_address: str = ERC721_TOKEN_TRANSFERS_CONTRACT_ADDRESS_QUERY_PARAMETER,
        from_block: Union[int,
                          str, None] = TOKEN_TRANSFERS_FROM_BLOCK_QUERY_PARAMETER,
        to_block: Union[int,
                        str, None] = TOKEN_TRANSFERS_TO_BLOCK_QUERY_PARAMETER,
        decode_events: bool = DECODE_EVENTS_QUERY_PARAMETER):
    """
    Returns the events of the given contract address under the provided filters.

    * from_block (optional): first block to filter from
    * to_block (optional): last block to filter to
    * decode_events (optional): decode events

    Events of proxy contracts cannot be decoded since the proxy contract ABI is not the matching one to the events, which is why an error is raised.
    """
    # TODO: remove infura when syced
    try:
        response = infura_execution_client.get_contract_events(
            contract_address, from_block, to_block, decode_events)
        return response
    except NoABIFound:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Contract not found (contract_address: {contract_address})"
        )
    except InvalidAddress:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid contract address (contract_address: {contract_address})"
        )
    except ABIEventFunctionNotFound:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"ABI event not found (contract_address: {contract_address})"
        )


@router.get("/transfers", responses={503: {"model": ErrorResponseModel}})
@connection_decorator
async def contract_transfers(
        contract_address: str = ERC721_TOKEN_TRANSFERS_CONTRACT_ADDRESS_QUERY_PARAMETER,
        from_block: Union[int,
                          str, None] = TOKEN_TRANSFERS_FROM_BLOCK_QUERY_PARAMETER,
        to_block: Union[int,
                        str, None] = TOKEN_TRANSFERS_TO_BLOCK_QUERY_PARAMETER,
        from_address: Union[str,
                            None] = ERC721_TOKEN_TRANSFERS_FROM_ADDRESS_QUERY_PARAMETER,
        to_address: Union[str,
                          None] = ERC721_TOKEN_TRANSFERS_TO_ADDRESS_QUERY_PARAMETER,
        value: Union[int,
                     None] = None,
        token_id: Union[int,
                        None] = ERC721_TOKEN_TRANSFERS_TOKEN_ID_QUERY_PARAMETER):
    """
    Returns the transactions of the given contract address under the provided filters.

    * from_block (optional): first block to filter from
    * to_block (optional): last block to filter to
    * from_address (optional): from address of the transfer
    * to_address (optional): to address of the transfer
    * value (optional): value of the transfer
    * token_id (optional): ID of the token

    Transfers can be filtered either by 'value' or 'token_id' depending on the token standard (ERC20, ERC721, ...) of the contract. It is not possible to provide both values at the same time.
    """
    if value is not None and token_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="It is not possible to pass both 'value' and 'token_id' at the same time."
        )

    argument_filters = {}
    if from_address is not None:
        argument_filters["from"] = from_address
    if to_address is not None:
        argument_filters["to"] = to_address
    if value is not None:
        argument_filters["value"] = value
    if token_id is not None:
        argument_filters["tokenId"] = token_id

    # TODO: remove infura when syced
    try:
        response = infura_execution_client.get_token_transfers(
            contract_address,
            from_block,
            to_block,
            argument_filters
        )
        return response
    except NoABIFound:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Contract not found (contract_address: {contract_address})"
        )
    except ABIFunctionNotFound:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Contract or ABI function not found (contract_address: {contract_address})"
        )


@router.get("/execute_function", responses={503: {"model": ErrorResponseModel}})
@connection_decorator
async def execute_contract_function(
        contract_address: str = CONTRACT_ADDRESS_QUERY_PARAMETER,
        function_name: str = CONTRACT_FUNCTION_QUERY_PARAMETER,
        function_args: list[Union[int, str, bool, float]
                            ] = CONTRACT_FUNCTION_ARGS_QUERY_PARAMETER):
    """
    Execute contract function by name and arguments.

    Will only work for call functions.
    """
    # TODO: remove infura when syced
    try:
        response = infura_execution_client.execute_contract_function(
            contract_address, function_name, *function_args)
        return {function_name: response}
    except NoABIFound:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Contract not found (contract_address: {contract_address})"
        )
    except ABIFunctionNotFound:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Contract or ABI function not found (contract_address: {contract_address})"
        )


@router.get("/list", responses={503: {"model": ErrorResponseModel}})
@connection_decorator
async def contract_list(
        token_standard: str = TOKEN_STANDARD_OPTIONAL_QUERY_PARAMETER,
        with_name: bool = False,
        with_symbol: bool = False,
        with_block_deployed: bool = False,
        with_total_supply: bool = False,
        with_abi: bool = False,
        limit: Union[int, None] = None):
    """
    Returns contract data safed in indexing db.

    * token_standard (optional): token standard of the contracts to be queried (ERC20, ERC721, ...)
    * with_name (optional): include name in response
    * with_symbol (optional): include name in response
    * with_total_supply (optional): include name in response
    * with_abi (optional): include name in response
    * limit (optional): limit the number of returned contract data
    """
    if limit is None:
        limit = 18446744073709551615

    response = sql_db_connector.query_contract_data(
        config.SQL_DATABASE_TABLE_CONTRACT, token_standard, with_name, with_symbol, with_block_deployed, with_total_supply, with_abi, limit)

    if with_total_supply:
        for data in response:
            if data["total_supply"] is not None:
                data["total_supply"] = str(data["total_supply"])

    return response


@router.get("/deploy_block", responses={503: {"model": ErrorResponseModel}})
@connection_decorator
async def contract_deploy_block(
        contract_address: str = ERC721_TOKEN_TRANSFERS_CONTRACT_ADDRESS_QUERY_PARAMETER):
    """
    Return block number of creation of contract.

    Returns null if no events are performed for the contract.
    """
    try:
        response = infura_execution_client.get_contract_deploy_block(
            contract_address)
        return {
            "block_number": response
        }
    except InvalidAddress:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid contract address (contract_address: {contract_address})"
        )


@router.get("/metadata", responses={503: {"model": ErrorResponseModel}})
@connection_decorator
async def contract_metadata(
        contract_address: str = ERC721_TOKEN_TRANSFERS_CONTRACT_ADDRESS_QUERY_PARAMETER):
    """
    Return contract metadata.
    Metadata may be empty if functions are not implemented by contract.
    """
    # TODO: remove infura when syced
    response = infura_execution_client.get_contract_metadata(
        contract_address)

    if response["total_supply"] is not None:
        response["total_supply"] = str(response["total_supply"])

    return response


@router.put("/transfers",
            status_code=status.HTTP_201_CREATED, responses={503: {"model": ErrorResponseModel}})
@connection_decorator
async def insert_contract_transactions(contract_address: str = ERC721_TOKEN_TRANSFERS_CONTRACT_ADDRESS_QUERY_PARAMETER,
                                       from_block: Union[int,
                                                         str, None] = TOKEN_TRANSFERS_FROM_BLOCK_QUERY_PARAMETER,
                                       to_block: Union[int,
                                                       str, None] = TOKEN_TRANSFERS_TO_BLOCK_QUERY_PARAMETER,
                                       from_address: Union[str,
                                                           None] = ERC721_TOKEN_TRANSFERS_FROM_ADDRESS_QUERY_PARAMETER,
                                       to_address: Union[str,
                                                         None] = ERC721_TOKEN_TRANSFERS_TO_ADDRESS_QUERY_PARAMETER,
                                       value: Union[int,
                                                    None] = ERC20_TOKEN_TRANSFERS_VALUE_QUERY_PARAMETER,
                                       token_id: Union[int,
                                                       None] = ERC721_TOKEN_TRANSFERS_TOKEN_ID_QUERY_PARAMETER,
                                       ):
    """
    Insert contract transactions into sql database.

    * from_block (optional): first block to filter from
    * to_block (optional): last block to filter to
    * from_address (optional): from address of the transfer
    * to_address (optional): to address of the transfer
    * value (optional): value of the transfer
    * token_id (optional): ID of the token

    Transfers can be filtered either by 'value' or 'token_id' depending on the token standard (ERC20, ERC721, ...) of the contract. It is not possible to provide both values at the same time.
    """
    if value is not None and token_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="It is not possible to pass both 'value' and 'token_id' at the same time."
        )

    argument_filters = {}
    if from_address is not None:
        argument_filters["from"] = from_address
    if to_address is not None:
        argument_filters["to"] = to_address
    if value is not None:
        argument_filters["value"] = value
    if token_id is not None:
        argument_filters["tokenId"] = token_id

    # TODO: remove infura when syced
    try:
        transactions = infura_execution_client.get_token_transfers(
            contract_address,
            from_block,
            to_block,
            argument_filters
        )
    except NoABIFound:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Contract not found (contract_address: {contract_address})"
        )
    except ABIFunctionNotFound:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Contract or ABI function not found (contract_address: {contract_address})"
        )
    for index, transaction in enumerate(transactions):
        transactions[index] = {
            "transaction_hash": transaction["transactionHash"],
            "contract_address": transaction["address"],
            "from_address": transaction["args"]["from"],
            "to_address": transaction["args"]["to"],
            "block_number": transaction["blockNumber"]
        }
        if "tokenId" in transaction["args"]:
            transactions[index]["token_id"] = transaction["args"]["tokenId"]
        if "value" in transaction["args"]:
            transactions[index]["value"] = transaction["args"]["value"]

    sql_db_connector.insert_many_transaction_data(
        config.SQL_DATABASE_TABLE_TRANSACTION, transactions)
