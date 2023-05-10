from fastapi import APIRouter, Depends, HTTPException, status
import app.config as config
from app.dependencies import get_current_active_user
from .schemas import *
from .parameters import *
from typing import Union
from app.connectors import execution_client, infura_execution_client, sql_db_connector, TokenStandard

router = APIRouter(
    prefix="/mainnet/contract",
    tags=["Smart Contract"],
    dependencies=[Depends(get_current_active_user)]
)


@router.get("/token_standard_abi")
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


@router.get("/contract_abi")
async def contract_abi(
        contract_address: str = CONTRACT_ADDRESS_QUERY_PARAMETER):
    """
    Returns the Contract Application Binary Interface (ABI) of a verified smart contract.
    """
    # TODO: remove infura when syced
    response = infura_execution_client.get_contract_abi(contract_address)

    if response is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Contract not found (contract_address: {contract_address})"
        )

    return response


@router.get("/implemented_token_standards")
async def contract_implemented_token_standards(
        contract_address: str = CONTRACT_ADDRESS_QUERY_PARAMETER):
    """
    Return if token standards are implemented by contract Application Binary Interface (ABI).
    """
    # TODO: remove infura when syced
    response = infura_execution_client.get_contract_implemented_token_standards(
        contract_address)

    if response is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Contract not found (contract_address: {contract_address})"
        )

    return response


@router.get("/contract_functions")
async def contract_functions(
        contract_address: str = CONTRACT_ADDRESS_QUERY_PARAMETER,
        as_abi: bool = AS_ABI_QUERY_PARAMETER):
    """
    Returns all contract functions.
    """
    # TODO: remove infura when syced
    response = infura_execution_client.get_all_contract_functions(
        contract_address, as_abi)

    return response


@router.get("/contract_events")
async def contract_events(
        contract_address: str = CONTRACT_ADDRESS_QUERY_PARAMETER,
        as_abi: bool = AS_ABI_QUERY_PARAMETER):
    """
    Returns all contract events.
    """
    # TODO: remove infura when syced
    response = infura_execution_client.get_all_contract_events(
        contract_address, as_abi)

    return response


@router.get("/execute_contract_function")
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
    response = infura_execution_client.execute_contract_function(
        contract_address, function_name, *function_args)

    if response is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Contract or ABI function not found (contract_address: {contract_address})"
        )

    return {function_name: response}


@router.get("/token_events")
async def token_events(
        contract_address: str = ERC721_TOKEN_TRANSFERS_CONTRACT_ADDRESS_QUERY_PARAMETER,
        from_block: Union[int,
                          str, None] = TOKEN_TRANSFERS_FROM_BLOCK_QUERY_PARAMETER,
        to_block: Union[int,
                        str, None] = TOKEN_TRANSFERS_TO_BLOCK_QUERY_PARAMETER):
    """
    Returns the transactions of the given ERC20 contract address under the provided filters.

    * from_block (optional): first block to filter from
    * to_block (optional): last block to filter to
    """
    # TODO: remove infura when syced
    response = infura_execution_client.get_contract_events(
        contract_address, from_block, to_block)

    return response


@router.get("/erc20_token_transfers")
async def erc20_token_transfers(
        contract_address: str = ERC20_TOKEN_TRANSFERS_CONTRACT_ADDRESS_QUERY_PARAMETER,
        from_block: Union[int,
                          str, None] = TOKEN_TRANSFERS_FROM_BLOCK_QUERY_PARAMETER,
        to_block: Union[int,
                        str, None] = TOKEN_TRANSFERS_TO_BLOCK_QUERY_PARAMETER,
        from_address: Union[str,
                            None] = ERC20_TOKEN_TRANSFERS_FROM_ADDRESS_QUERY_PARAMETER,
        to_address: Union[str,
                          None] = ERC20_TOKEN_TRANSFERS_TO_ADDRESS_QUERY_PARAMETER,
        value: Union[int,
                     None] = ERC20_TOKEN_TRANSFERS_VALUE_QUERY_PARAMETER):
    """
    Returns the transactions of the given ERC20 contract address under the provided filters.

    * from_block (optional): first block to filter from
    * to_block (optional): last block to filter to
    * from_address (optional): from address of the transfer
    * to_address (optional): to address of the transfer
    * value (optional): value of the transfer
    """
    argument_filters = {}
    if from_address is not None:
        argument_filters["from"] = from_address
    if to_address is not None:
        argument_filters["to"] = to_address
    if value is not None:
        argument_filters["value"] = value

    # TODO: remove infura when syced
    response = infura_execution_client.get_token_transfers(
        contract_address,
        from_block,
        to_block,
        argument_filters
    )

    return response


@router.get("/erc721_token_transfers")
async def erc721_token_transfers(
        contract_address: str = ERC721_TOKEN_TRANSFERS_CONTRACT_ADDRESS_QUERY_PARAMETER,
        from_block: Union[int,
                          str, None] = TOKEN_TRANSFERS_FROM_BLOCK_QUERY_PARAMETER,
        to_block: Union[int,
                        str, None] = TOKEN_TRANSFERS_TO_BLOCK_QUERY_PARAMETER,
        from_address: Union[str,
                            None] = ERC721_TOKEN_TRANSFERS_FROM_ADDRESS_QUERY_PARAMETER,
        to_address: Union[str,
                          None] = ERC721_TOKEN_TRANSFERS_TO_ADDRESS_QUERY_PARAMETER,
        token_id: Union[int,
                        None] = ERC721_TOKEN_TRANSFERS_TOKEN_ID_QUERY_PARAMETER):
    """
    Returns the transactions of the given ERC721 contract address under the provided filters.

    * from_block (optional): first block to filter from
    * to_block (optional): last block to filter to
    * from_address (optional): from address of the transfer
    * to_address (optional): to address of the transfer
    * token_id (optional): ID of the token
    """
    argument_filters = {}
    if from_address is not None:
        argument_filters["from"] = from_address
    if to_address is not None:
        argument_filters["to"] = to_address
    if token_id is not None:
        argument_filters["tokenId"] = token_id

    # TODO: remove infura when syced
    response = infura_execution_client.get_token_transfers(
        contract_address,
        from_block,
        to_block,
        argument_filters
    )

    return response


@router.get("/erc20_contracts")
async def erc20_contracts(
        with_name: bool = False,
        with_symbol: bool = False,
        with_block_deployed: bool = False,
        with_total_supply: bool = False,
        with_abi: bool = False,
        limit: Union[int, None] = None):
    """
    Returns ERC20 contract data safed in indexing db.

    * with_name (optional): include name in response
    * with_symbol (optional): include name in response
    * with_total_supply (optional): include name in response
    * with_abi (optional): include name in response
    * limit (optional): limit the number of returned contract data
    """
    if limit is None:
        limit = 18446744073709551615

    response = sql_db_connector.query_contract_data(
        config.SQL_DATABASE_TABLE_CONTRACT, with_name, with_symbol, with_block_deployed, with_total_supply, with_abi, limit)

    if with_total_supply:
        for data in response:
            if data["total_supply"] is not None:
                data["total_supply"] = str(data["total_supply"])

    return response


@router.get("/erc721_contracts")
async def erc721_contracts(
        with_name: bool = False,
        with_symbol: bool = False,
        with_block_deployed: bool = False,
        with_total_supply: bool = False,
        with_abi: bool = False,
        limit: Union[int, None] = None):
    """
    Returns ERC721 contract data safed in indexing db.

    * with_name (optional): include name in response
    * with_symbol (optional): include name in response
    * with_total_supply (optional): include name in response
    * with_abi (optional): include name in response
    * limit (optional): limit the number of returned contract data
    """
    if limit is None:
        limit = 18446744073709551615

    response = sql_db_connector.query_contract_data(
        config.SQL_DATABASE_TABLE_CONTRACT, with_name, with_symbol, with_block_deployed, with_total_supply, with_abi, limit)

    if with_total_supply:
        for data in response:
            if data["total_supply"] is not None:
                data["total_supply"] = str(data["total_supply"])

    return response


@router.get("/contract_deploy_block")
async def contract_deploy_block(
        contract_address: str = ERC721_TOKEN_TRANSFERS_CONTRACT_ADDRESS_QUERY_PARAMETER):
    """
    Return block number of creation of contract.

    Returns null if no events are performed for the contract.
    """
    response = infura_execution_client.get_contract_deploy_block(
        contract_address)

    return {
        "block_number": response
    }


@router.get("/contract_metadata")
async def contract_metadata(
        contract_address: str = ERC721_TOKEN_TRANSFERS_CONTRACT_ADDRESS_QUERY_PARAMETER):
    """
    Return contract metadata.
    Metadata may be empty if functions are not implemented by contract.
    """
    # TODO: remove infura when syced
    response = infura_execution_client.get_contract_metadata(
        contract_address)

    response["total_supply"] = str(response["total_supply"])

    return response


@router.put("/insert_erc721_contract_transactions",
            status_code=status.HTTP_201_CREATED)
async def erc721_contract_transactions(contract_address: str = ERC721_TOKEN_TRANSFERS_CONTRACT_ADDRESS_QUERY_PARAMETER,
                                       from_block: Union[int,
                                                         str, None] = TOKEN_TRANSFERS_FROM_BLOCK_QUERY_PARAMETER,
                                       to_block: Union[int,
                                                       str, None] = TOKEN_TRANSFERS_TO_BLOCK_QUERY_PARAMETER,
                                       from_address: Union[str,
                                                           None] = ERC721_TOKEN_TRANSFERS_FROM_ADDRESS_QUERY_PARAMETER,
                                       to_address: Union[str,
                                                         None] = ERC721_TOKEN_TRANSFERS_TO_ADDRESS_QUERY_PARAMETER,
                                       token_id: Union[int,
                                                       None] = ERC721_TOKEN_TRANSFERS_TOKEN_ID_QUERY_PARAMETER,
                                       ):
    """
    Insert contract transactions into sql database.

    * from_block (optional): first block to filter from
    * to_block (optional): last block to filter to
    * from_address (optional): from address of the transfer
    * to_address (optional): to address of the transfer
    * token_id (optional): ID of the token
    """
    argument_filters = {}
    if from_address is not None:
        argument_filters["from"] = from_address
    if to_address is not None:
        argument_filters["to"] = to_address
    if token_id is not None:
        argument_filters["tokenId"] = token_id

    # TODO: remove infura when syced
    transactions = infura_execution_client.get_token_transfers(
        contract_address,
        from_block,
        to_block,
        argument_filters
    )

    for index, transaction in enumerate(transactions):
        transactions[index] = {
            "transaction_hash": transaction["transactionHash"],
            "contract_address": transaction["address"],
            "token_id": transaction["args"]["tokenId"],
            "from_address": transaction["args"]["from"],
            "to_address": transaction["args"]["to"],
            "block_number": transaction["blockNumber"]
        }

    sql_db_connector.insert_many_transaction_data(
        config.SQL_DATABASE_TABLE_TRANSACTION, transactions)


@router.put("/insert_erc20_contract_transactions",
            status_code=status.HTTP_201_CREATED)
async def erc20_contract_transactions(contract_address: str = ERC20_TOKEN_TRANSFERS_CONTRACT_ADDRESS_QUERY_PARAMETER,
                                      from_block: Union[int,
                                                        str, None] = TOKEN_TRANSFERS_FROM_BLOCK_QUERY_PARAMETER,
                                      to_block: Union[int,
                                                      str, None] = TOKEN_TRANSFERS_TO_BLOCK_QUERY_PARAMETER,
                                      from_address: Union[str,
                                                          None] = ERC20_TOKEN_TRANSFERS_FROM_ADDRESS_QUERY_PARAMETER,
                                      to_address: Union[str,
                                                        None] = ERC20_TOKEN_TRANSFERS_TO_ADDRESS_QUERY_PARAMETER,
                                      value: Union[int,
                                                   None] = ERC20_TOKEN_TRANSFERS_VALUE_QUERY_PARAMETER,
                                      ):
    """
    Insert contract transactions into sql database.

    * from_block (optional): first block to filter from
    * to_block (optional): last block to filter to
    * from_address (optional): from address of the transfer
    * to_address (optional): to address of the transfer
    * value (optional): value of the transfer
    """
    argument_filters = {}
    if from_address is not None:
        argument_filters["from"] = from_address
    if to_address is not None:
        argument_filters["to"] = to_address
    if value is not None:
        argument_filters["value"] = value

    # TODO: remove infura when syced
    transactions = infura_execution_client.get_token_transfers(
        contract_address,
        from_block,
        to_block,
        argument_filters
    )

    for index, transaction in enumerate(transactions):
        transactions[index] = {
            "transaction_hash": transaction["transactionHash"],
            "contract_address": transaction["address"],
            "value": transaction["args"]["value"],
            "from_address": transaction["args"]["from"],
            "to_address": transaction["args"]["to"],
            "block_number": transaction["blockNumber"]
        }

    sql_db_connector.insert_many_transaction_data(
        config.SQL_DATABASE_TABLE_TRANSACTION, transactions)
