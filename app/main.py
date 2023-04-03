from datetime import datetime, timedelta
from typing import Union
import json

from fastapi import Depends, FastAPI, HTTPException, status, Request
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.api_metadata.api_data_models import *
from app.api_metadata.api_response_models import *
from app.api_metadata.api_query_parameters import *
import app.api_metadata.api_metadata as api_metadata

import app.config as config
from app.execution_client_connector import ExecutionClientConnector, TokenStandard
from app.consensus_client_connector import ConsensusClientConnector
from app.sql_database_connector import SqlDatabaseConnector
from app.users_db import users_db
import app.evaluation as evaluation
import app.db_metadata.sql_tables as tables

# init sql database connector
sql_db_connector = SqlDatabaseConnector(
    config.SQL_DATABASE_HOST,
    config.SQL_DATABASE_PORT,
    config.SQL_DATABASE_USER,
    config.SQL_DATABASE_PASSWORD
)
sql_db_connector.use_database(config.SQL_DATABASE_NAME)
sql_db_connector.create_table(tables.CONTRACT_TABLE)


execution_client_url = f"http://{config.EXECUTION_CLIENT_IP}:{config.EXECUTION_CLIENT_PORT}"

# TODO: change url from infura
infura_url = "https://mainnet.infura.io/v3/c2762ad3b91949a099c826439f9dc5c6"

# init token standards
token_standards = {}
for token_standard in TokenStandard:
    with open(f"app/token_standard/{token_standard.name}.json", "r") as f:
        token_standards[token_standard.name] = json.load(f)

execution_client = ExecutionClientConnector(
    infura_url, config.ETHERSCAN_URL, config.ETHERSCAN_API_KEY, token_standards, sql_db_connector, config.SQL_DATABASE_TABLE_CONTRACT)

consensus_client = ConsensusClientConnector(
    config.CONSENCUS_CLIENT_IP, config.CONSENSUS_CLIENT_PORT)


app = FastAPI(
    title=api_metadata.API_TITLE,
    description=api_metadata.API_DESCIPTION,
    version=api_metadata.API_VERSION,
    contact={
        "name": api_metadata.API_CONTACT_NAME,
        "email": api_metadata.API_CONTACT_EMAIL
    },
    openapi_tags=api_metadata.API_TAGS_METADATA,
    docs_url=None,
    redoc_url=None
)
app.mount("/static", StaticFiles(directory="static"), name="static")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: Union[str, None]):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    elif not verify_password(password, user.hashed_password):
        return False
    else:
        return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.API_AUTHENTICATION_SECRET_KEY,
                             algorithm=config.API_AUTHENTICATION_ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.API_AUTHENTICATION_SECRET_KEY, algorithms=[
                             config.API_AUTHENTICATION_ALGORITHM])
        username: Union[str, None] = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# Authentication and Users

@app.post("/token", response_model=Token, tags=["Authentication and Users"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(
        users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=config.API_AUTHENTICATION_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me", response_model=User, tags=["Authentication and Users"])
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


# Docs

@app.get("/docs", include_in_schema=False)
async def swagger_ui_html(req: Request) -> HTMLResponse:
    root_path = req.scope.get("root_path", "").rstrip("/")
    openapi_url = root_path + app.openapi_url
    oauth2_redirect_url = app.swagger_ui_oauth2_redirect_url
    if oauth2_redirect_url:
        oauth2_redirect_url = root_path + oauth2_redirect_url

    return get_swagger_ui_html(
        openapi_url=openapi_url,
        title=api_metadata.API_TITLE,
        oauth2_redirect_url=oauth2_redirect_url,
        init_oauth=app.swagger_ui_init_oauth,
        swagger_favicon_url="/static/favicon.ico",
        swagger_ui_parameters=api_metadata.API_SWAGGER_UI_PARAMETERS
    )


@app.get("/redoc", include_in_schema=False)
async def redoc_ui_html():
    return get_redoc_html(
        openapi_url="/openapi.json",
        title=api_metadata.API_TITLE,
        redoc_favicon_url="/static/favicon.ico"
    )


# Execution Client Gossip Methods

@app.get("/execution_client/gossip/block_number", tags=["Execution Client Gossip Methods"], response_model=ExecutionClientResponseModelBlockNumber)
async def execution_client_block_number(current_user: User = Depends(get_current_active_user)):
    """
    Returns the number of most recent block.
    """
    response = execution_client.block_number()
    return response


# Execution Client State Methods

@app.get("/execution_client/state/default_account", tags=["Execution Client State Methods"], response_model=ExecutionClientResponseModelDefaultAccount)
async def execution_client_default_account(current_user: User = Depends(get_current_active_user)):
    """
    Returns the ethereum address that will be used as the default from address for all transactions.

    Defaults to empty.
    """
    response = execution_client.default_account()
    return response


@app.get("/execution_client/state/default_block", tags=["Execution Client State Methods"], response_model=ExecutionClientResponseModelDefaultBlock)
async def execution_client_default_block(current_user: User = Depends(get_current_active_user)):
    """
    Returns the default block number that will be used for any RPC methods that accept a block identifier.

    Defaults to 'latest'.
    """
    response = execution_client.default_block()
    return response


@app.get("/execution_client/state/syncing", tags=["Execution Client State Methods"], response_model=Union[ExecutionClientResponseModelSyncingTrue, ExecutionClientResponseModelSyncingFalse])
async def execution_client_syncing(current_user: User = Depends(get_current_active_user)):
    """
    Returns either False if the node is not syncing or a dictionary showing sync status.
    """
    response = execution_client.syncing()
    return response


@app.get("/execution_client/state/mining", tags=["Execution Client State Methods"], response_model=ExecutionClientResponseModelMining)
async def execution_client_mining(current_user: User = Depends(get_current_active_user)):
    """
    Returns boolean as to whether the node is currently mining.
    """
    response = execution_client.mining()
    return response


@app.get("/execution_client/state/hashrate", tags=["Execution Client State Methods"], response_model=ExecutionClientResponseModelHashrate)
async def execution_client_hashrate(current_user: User = Depends(get_current_active_user)):
    """
    Returns the current number of hashes per second the node is mining with.
    """
    response = execution_client.hashrate()
    return response


@app.get("/execution_client/state/max_priority_fee", tags=["Execution Client State Methods"], response_model=ExecutionClientResponseModelMaxPriorityFee)
async def execution_client_max_priority_fee(current_user: User = Depends(get_current_active_user)):
    """
    Returns a suggestion for a max priority fee for dynamic fee transactions in Wei.
    """
    response = execution_client.max_priority_fee()
    return response


@app.get("/execution_client/state/accounts", tags=["Execution Client State Methods"], response_model=ExecutionClientResponseModelAccounts)
async def execution_client_accounts(current_user: User = Depends(get_current_active_user)):
    """
    Returns the list of known accounts.
    """
    response = execution_client.accounts()
    return response


@app.get("/execution_client/state/chain_id", tags=["Execution Client State Methods"], response_model=ExecutionClientResponseModelChainId)
async def execution_client_chain_id(current_user: User = Depends(get_current_active_user)):
    """
    Returns an integer value for the currently configured “Chain Id” value introduced in EIP-155.

    Returns None if no Chain Id is available.
    """
    response = execution_client.chain_id()

    return response


@app.get("/execution_client/state/get_api_version", tags=["Execution Client State Methods"], response_model=ExecutionClientResponseModelGetApiVersion)
async def execution_client_get_api_version(current_user: User = Depends(get_current_active_user)):
    """
    Returns the id of the current API version.
    """
    response = execution_client.get_api_version()
    return response


@app.get("/execution_client/state/get_client_version", tags=["Execution Client State Methods"], response_model=ExecutionClientResponseModelGetClientVersion)
async def execution_client_get_client_version(current_user: User = Depends(get_current_active_user)):
    """
    Returns the id of the current Ethereum protocol version.
    """
    response = execution_client.get_client_version()
    return response


@app.get("/execution_client/state/get_balance", tags=["Execution Client State Methods"], response_model=ExecutionClientResponseModelGetBalance)
async def execution_client_get_balance(
        wallet_address: str = WALLET_ADDRESS_QUERY_PARAMETER,
        block_identifier: Union[int, str,
                                None] = BLOCK_IDENTIFIER_OPTIONAL_QUERY_PARAMETER,
        current_user: User = Depends(get_current_active_user)):
    """
    Returns the balance of the given wallet_address at the block specified by block_identifier.

    wallet_address may be a checksum address or an ENS name
    """
    response = execution_client.get_balance(wallet_address, block_identifier)
    return response


@app.get("/execution_client/state/get_block_number", tags=["Execution Client State Methods"], response_model=ExecutionClientResponseModelGetBlockNumber)
async def execution_client_get_block_number(current_user: User = Depends(get_current_active_user)):
    """
    Returns the number of the most recent block.
    """
    response = execution_client.get_block_number()
    return response


@app.get("/execution_client/state/get_storage_at", tags=["Execution Client State Methods"], response_model=ExecutionClientResponseModelGetStorageAt)
async def execution_client_get_storage_at(
        wallet_address: str = WALLET_ADDRESS_QUERY_PARAMETER,
        position: int = POSITION_QUERY_PARAMETER,
        block_identifier: Union[int, str,
                                None] = BLOCK_IDENTIFIER_OPTIONAL_QUERY_PARAMETER,
        current_user: User = Depends(get_current_active_user)):
    """
    Returns the value from a storage position for the given wallet_address at the block specified by block_identifier.

    wallet_address may be a checksum address or an ENS name
    """
    response = execution_client.get_storage_at(
        wallet_address, position, block_identifier)
    return response


@app.get("/execution_client/state/get_code", tags=["Execution Client State Methods"], response_model=ExecutionClientResponseModelGetCode)
async def execution_client_get_code(
        wallet_address: str = WALLET_ADDRESS_QUERY_PARAMETER,
        current_user: User = Depends(get_current_active_user)):
    """
    Returns the bytecode for the given wallet_address at the block specified by block_identifier.

    wallet_address may be a checksum address or an ENS name
    """
    response = execution_client.get_code(wallet_address)
    return response


@app.get("/execution_client/state/get_transaction_count", tags=["Execution Client State Methods"], response_model=ExecutionClientResponseModelGetTransactionCount)
async def execution_client_get_transaction_count(
        wallet_address: str = WALLET_ADDRESS_QUERY_PARAMETER,
        block_identifier: Union[int, str,
                                None] = BLOCK_IDENTIFIER_OPTIONAL_QUERY_PARAMETER,
        current_user: User = Depends(get_current_active_user)):
    """
    Returns the number of transactions that have been sent from wallet_address as of the block specified by block_identifier.

    wallet_address may be a checksum address or an ENS name
    """
    reponse = execution_client.get_transaction_count(
        wallet_address, block_identifier)
    return reponse


@app.get("/execution_client/state/estimate_gas", tags=["Execution Client State Methods"], response_model=ExecutionClientResponseModelEstimateGas)
async def execution_client_estimate_gas(
        from_address: str = FROM_ADDRESS_QUERY_PARAMETER,
        to_address: str = TO_ADDRESS_QUERY_PARAMETER,
        value: int = TRANSACTION_VALUE_QUERY_PARAMETER,
        current_user: User = Depends(get_current_active_user)):
    """
    Executes the given transaction locally without creating a new transaction on the blockchain. Returns amount of gas consumed by execution which can be used as a gas estimate.

    The transaction and block_identifier parameters are handled in the same manner as the send_transaction() method.
    """
    # TODO: not working -> node not fully synced
    response = execution_client.estimate_gas(from_address, to_address, value)
    return response


# Execution Client History Methods

@app.get("/execution_client/history/get_block_transaction_count",
         tags=["Execution Client History Methods"],
         responses={200: {"model": ExecutionClientResponseModelGetBlockTransactionCount}, 400: {"model": ErrorResponseModel}})
async def execution_client_get_block_transaction_count(
        block_identifier: Union[int, str] = BLOCK_IDENTIFIER_QUERY_PARAMETER,
        current_user: User = Depends(get_current_active_user)):
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


@app.get("/execution_client/history/get_uncle_count",
         tags=["Execution Client History Methods"],
         responses={200: {"model": ExecutionClientResponseModelGetUncleCount}, 400: {"model": ErrorResponseModel}})
async def execution_client_get_uncle_count(
        block_identifier: Union[int,
                                str] = BLOCK_IDENTIFIER_UNCLE_QUERY_PARAMETER,
        current_user: User = Depends(get_current_active_user)):
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


@app.get("/execution_client/history/get_block",
         tags=["Execution Client History Methods"],
         responses={200: {"model": Union[ExecutionClientResponseModelGetBlockFalse, ExecutionClientResponseModelGetBlockTrue]}, 400: {"model": ErrorResponseModel}})
async def execution_client_get_block(
        block_identifier: Union[int, str,
                                None] = BLOCK_IDENTIFIER_OPTIONAL_QUERY_PARAMETER,
        full_transactions: bool = FULL_TRANSACTION_QUERY_PARAMETER,
        current_user: User = Depends(get_current_active_user)):
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


@app.get("/execution_client/history/get_transaction",
         tags=["Execution Client History Methods"],
         responses={200: {"model": ExecutionClientResponseModelGetTransaction}, 400: {"model": ErrorResponseModel}})
async def execution_client_get_transaction(
        transaction_hash: str = TRANSACTION_HASH_QUERY_PARAMETER,
        current_user: User = Depends(get_current_active_user)):
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


@ app.get("/execution_client/history/get_transaction_by_block",
          tags=["Execution Client History Methods"],
          responses={200: {"model": ExecutionClientResponseModelGetTransactionByBlock}, 400: {"model": ErrorResponseModel}})
async def execution_client_get_transaction_by_block(
        block_identifier: Union[int, str] = BLOCK_IDENTIFIER_QUERY_PARAMETER,
        transaction_index: int = TRANSACTION_INDEX_QUERY_PARAMETER,
        current_user: User = Depends(get_current_active_user)):
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


@ app.get("/execution_client/history/get_transaction_receipt",
          tags=["Execution Client History Methods"],
          responses={200: {"model": ExecutionClientResponseModelGetTransactionReceipt}, 400: {"model": ErrorResponseModel}})
async def execution_client_get_transaction_receipt(
        transaction_hash: str = TRANSACTION_HASH_QUERY_PARAMETER,
        current_user: User = Depends(get_current_active_user)):
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


@ app.get("/execution_client/history/get_uncle_by_block",
          tags=["Execution Client History Methods"],
          responses={200: {"model": ExecutionClientResponseModelGetUncleByBlock}, 400: {"model": ErrorResponseModel}})
async def execution_client_get_uncle_by_block(
        block_identifier: Union[int,
                                str] = BLOCK_IDENTIFIER_UNCLE_QUERY_PARAMETER,
        uncle_index: int = UNCLE_INDEX_QUERY_PARAMETER,
        current_user: User = Depends(get_current_active_user)):
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


# Execution Client Contract Methods

@app.get("/execution_client/contract/get_token_standard_abi",
         tags=["Execution Client Contract Methods"])
async def execution_client_get_token_standard_abi(
    token_standard: TokenStandard = TOKEN_STANDARD_QUERY_PARAMETER,
    current_user: User = Depends(get_current_active_user)
):
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


@app.get("/execution_client/contract/get_contract_abi",
         tags=["Execution Client Contract Methods"])
async def execution_client_get_contract_abi(
        contract_address: str = CONTRACT_ADDRESS_QUERY_PARAMETER,
        current_user: User = Depends(get_current_active_user)):
    """
    Returns the Contract Application Binary Interface (ABI) of a verified smart contract.
    """
    response = execution_client.get_contract_abi(contract_address)

    if response is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Contract not found (contract_address: {contract_address})"
        )

    return response


@app.get("/execution_client/contract/get_implemented_token_standards",
         tags=["Execution Client Contract Methods"])
async def execution_client_get_contract_implemented_token_standards(
        contract_address: str = CONTRACT_ADDRESS_QUERY_PARAMETER,
        current_user: User = Depends(get_current_active_user)):
    """
    Return if token standards are implemented by contract Application Binary Interface (ABI).
    """
    response = execution_client.get_contract_implemented_token_standards(
        contract_address)

    if response is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Contract not found (contract_address: {contract_address})"
        )

    return response


@app.get("/execution_client/contract/get_contract_functions",
         tags=["Execution Client Contract Methods"])
async def execution_client_get_contract_functions(
        contract_address: str = CONTRACT_ADDRESS_QUERY_PARAMETER,
        as_abi: bool = AS_ABI_QUERY_PARAMETER,
        current_user: User = Depends(get_current_active_user)):
    """
    Returns all contract functions.
    """
    response = execution_client.get_all_contract_functions(
        contract_address, as_abi)

    return response


@app.get("/execution_client/contract/get_contract_events",
         tags=["Execution Client Contract Methods"])
async def execution_client_get_contract_events(
        contract_address: str = CONTRACT_ADDRESS_QUERY_PARAMETER,
        as_abi: bool = AS_ABI_QUERY_PARAMETER,
        current_user: User = Depends(get_current_active_user)):
    """
    Returns all contract events.
    """
    response = execution_client.get_all_contract_events(
        contract_address, as_abi)

    return response


@app.get("/execution_client/contract/execute_contract_function",
         tags=["Execution Client Contract Methods"])
async def execution_client_execute_contract_function(
        contract_address: str = CONTRACT_ADDRESS_QUERY_PARAMETER,
        function_name: str = CONTRACT_FUNCTION_QUERY_PARAMETER,
        function_args: list[Union[int, str, bool, float]
                            ] = CONTRACT_FUNCTION_ARGS_QUERY_PARAMETER,
        current_user: User = Depends(get_current_active_user)):
    """
    Execute contract function by name and arguments.

    Will only work for call functions.
    """
    response = execution_client.execute_contract_function(
        contract_address, function_name, *function_args)

    if response is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Contract or ABI function not found (contract_address: {contract_address})"
        )

    return {function_name: response}


@app.get("/execution_client/contract/get_token_events",
         tags=["Execution Client Contract Methods"])
async def execution_client_get_token_events(
        contract_address: str = ERC721_TOKEN_TRANSFERS_CONTRACT_ADDRESS_QUERY_PARAMETER,
        from_block: Union[int,
                          str, None] = TOKEN_TRANSFERS_FROM_BLOCK_QUERY_PARAMETER,
        to_block: Union[int,
                        str, None] = TOKEN_TRANSFERS_TO_BLOCK_QUERY_PARAMETER,
        current_user: User = Depends(get_current_active_user)):
    """
    Returns the transactions of the given ERC20 contract address under the provided filters.

    * from_block (optional): first block to filter from
    * to_block (optional): last block to filter to
    """
    response = execution_client.get_token_events(
        contract_address, from_block, to_block)

    return response


@app.get("/execution_client/contract/get_erc20_token_transfers",
         tags=["Execution Client Contract Methods"])
async def execution_client_get_erc20_token_transfers(
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
                     None] = ERC20_TOKEN_TRANSFERS_VALUE_QUERY_PARAMETER,
        current_user: User = Depends(get_current_active_user)):
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

    response = execution_client.get_token_transfers(
        contract_address,
        from_block,
        to_block,
        argument_filters
    )

    return response


@app.get("/execution_client/contract/get_erc721_token_transfers",
         tags=["Execution Client Contract Methods"])
async def execution_client_get_erc721_token_transfers(
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
                        None] = ERC721_TOKEN_TRANSFERS_TOKEN_ID_QUERY_PARAMETER,
        current_user: User = Depends(get_current_active_user)):
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

    response = execution_client.get_token_transfers(
        contract_address,
        from_block,
        to_block,
        argument_filters
    )

    return response


@app.get("/execution_client/contract/get_contract_metadata",
         tags=["Execution Client Contract Methods"])
async def execution_client_get_contract_metadata(
        contract_address: str = ERC721_TOKEN_TRANSFERS_CONTRACT_ADDRESS_QUERY_PARAMETER,
        current_user: User = Depends(get_current_active_user)):
    """
    Return contract metadata.
    Metadata may be empty if functions are not implemented by contract.
    """
    response = execution_client.get_contract_metadata(
        contract_address)

    return response


# Consensus Client Beacon Methods

@ app.get("/consensus_client/beacon/get_genesis", tags=["Consensus Client Beacon Methods"], response_model=ConsensusClientResponseModelGetGenesis)
async def consensus_client_get_genesis(current_user: User = Depends(get_current_active_user)):
    """
    Retrieve details of the chain's genesis which can be used to identify chain.
    """
    response = consensus_client.get_genesis()
    return response


@ app.get("/consensus_client/beacon/get_hash_root", tags=["Consensus Client Beacon Methods"], response_model=ConsensusClientResponseModelGetHashRoot)
async def consensus_client_get_hash_root(
        state_id: str = "head",
        current_user: User = Depends(get_current_active_user)):
    """
    Calculates HashTreeRoot for state with given 'stateId'. If stateId is root, same value will be returned.
    """
    response = consensus_client.get_hash_root(state_id)
    return response


@ app.get("/consensus_client/beacon/get_fork_data", tags=["Consensus Client Beacon Methods"], response_model=ConsensusClientResponseModelGetForkData)
async def consensus_client_get_fork_data(
        state_id: str = "head",
        current_user: User = Depends(get_current_active_user)):
    """
    Returns Fork object for state with given 'stateId'.
    """
    response = consensus_client.get_fork_data(state_id)
    return response


@ app.get("/consensus_client/beacon/get_finality_checkpoint", tags=["Consensus Client Beacon Methods"], response_model=ConsensusClientResponseModelGetFinalityCheckpoint)
async def consensus_client_get_finality_checkpoint(
        state_id: str = "head",
        current_user: User = Depends(get_current_active_user)):
    """
    Returns finality checkpoints for state with given 'stateId'. In case finality is not yet achieved, checkpoint should return epoch 0 and ZERO_HASH as root.
    """
    response = consensus_client.get_finality_checkpoint(state_id)
    return response


@ app.get("/consensus_client/beacon/get_validators", tags=["Consensus Client Beacon Methods"], response_model=ConsensusClientResponseModelGetValidators)
async def consensus_client_get_validators(
        state_id: str = STATE_ID_QUERY_PARAMETER,
        current_user: User = Depends(get_current_active_user)):
    """
    Returns filterable list of validators with their balance, status and index.

    Information will be returned for all indices or public key that match known validators. If an index or public key does not match any known validator, no information will be returned but this will not cause an error. There are no guarantees for the returned data in terms of ordering; both the index and public key are returned for each validator, and can be used to confirm for which inputs a response has been returned.
    """
    # TODO: not working
    response = consensus_client.get_validators(state_id)
    return response


@ app.get("/consensus_client/beacon/get_validator", tags=["Consensus Client Beacon Methods"], response_model=ConsensusClientResponseModelGetValidator)
async def consensus_client_get_validator(
        validator_id: int = VALIDATOR_ID_QUERY_PARAMETER,
        state_id: str = STATE_ID_QUERY_PARAMETER,
        current_user: User = Depends(get_current_active_user)):
    """
    Returns validator specified by state and id or public key along with status and balance.
    """
    response = consensus_client.get_validator(validator_id, state_id)
    return response


@ app.get("/consensus_client/beacon/get_validator_balances", tags=["Consensus Client Beacon Methods"], response_model=ConsensusClientResponseModelGetValidatorBalances)
async def consensus_client_get_validator_balances(
        state_id: str = STATE_ID_QUERY_PARAMETER,
        current_user: User = Depends(get_current_active_user)):
    """
    Returns filterable list of validators balances.

    Balances will be returned for all indices or public key that match known validators. If an index or public key does not match any known validator, no balance will be returned but this will not cause an error. There are no guarantees for the returned data in terms of ordering; the index and is returned for each balance, and can be used to confirm for which inputs a response has been returned.
    """
    response = consensus_client.get_validator_balances(state_id)
    return response


@ app.get("/consensus_client/beacon/get_epoch_committees", tags=["Consensus Client Beacon Methods"], response_model=ConsensusClientResponseModelGetEpochCommittees)
async def consensus_client_get_epoch_committees(
        state_id: str = STATE_ID_QUERY_PARAMETER,
        current_user: User = Depends(get_current_active_user)):
    """
    Retrieves the committees for the given state.
    """
    response = consensus_client.get_epoch_committees(state_id)
    return response


@ app.get("/consensus_client/beacon/get_block_headers", tags=["Consensus Client Beacon Methods"], response_model=ConsensusClientResponseModelGetBlockHeaders)
async def consensus_client_get_block_headers(current_user: User = Depends(get_current_active_user)):
    """
    Retrieves block headers matching given query. By default it will fetch current head slot blocks.
    """
    response = consensus_client.get_block_headers()
    return response


@ app.get("/consensus_client/beacon/get_block_header", tags=["Consensus Client Beacon Methods"], response_model=ConsensusClientResponseModelGetBlockHeader)
async def consensus_client_get_block_header(
        block_id: Union[int, str] = BLOCK_ID_QUERY_PARAMETER,
        current_user: User = Depends(get_current_active_user)):
    """
    Retrieves block header for given block id.
    """
    response = consensus_client.get_block_header(block_id)
    return response


@ app.get("/consensus_client/beacon/get_block", tags=["Consensus Client Beacon Methods"], response_model=ConsensusClientResponseModelGetBlock)
async def consensus_client_get_block(
        block_id: Union[int, str] = BLOCK_ID_QUERY_PARAMETER,
        current_user: User = Depends(get_current_active_user)):
    """
    Retrieves block details for given block id. Depending on Accept header it can be returned either as json or as bytes serialized by SSZ
    """
    response = consensus_client.get_block(block_id)
    return response


@ app.get("/consensus_client/beacon/get_block_root", tags=["Consensus Client Beacon Methods"], response_model=ConsensusClientResponseModelGetBlockRoot)
async def consensus_client_get_block_root(
        block_id: Union[int, str] = BLOCK_ID_QUERY_PARAMETER,
        current_user: User = Depends(get_current_active_user)):
    """
    Retrieves hashTreeRoot of BeaconBlock/BeaconBlockHeader
    """
    response = consensus_client.get_block_root(block_id)
    return response


@ app.get("/consensus_client/beacon/get_block_attestations", tags=["Consensus Client Beacon Methods"], response_model=ConsensusClientResponseModelGetBlockAttestations)
async def consensus_client_get_block_attestations(
        block_id: Union[int, str] = BLOCK_ID_QUERY_PARAMETER,
        current_user: User = Depends(get_current_active_user)):
    """
    Retrieves attestation included in requested block.
    """
    response = consensus_client.get_block_attestations(block_id)
    return response


@ app.get("/consensus_client/beacon/get_attestations", tags=["Consensus Client Beacon Methods"], response_model=ConsensusClientResponseModelGetAttestations)
async def consensus_client_get_attestations(current_user: User = Depends(get_current_active_user)):
    """
    Retrieves attestations known by the node but not necessarily incorporated into any block
    """
    response = consensus_client.get_attestations()
    return response


@ app.get("/consensus_client/beacon/get_attester_slashings", tags=["Consensus Client Beacon Methods"], response_model=ConsensusClientResponseModelGetAttesterSlashings)
async def consensus_client_get_attester_slashings(current_user: User = Depends(get_current_active_user)):
    """
    Retrieves attester slashings known by the node but not necessarily incorporated into any block
    """
    # TODO: not working yet (empty response)
    response = consensus_client.get_attester_slashings()
    return response


@ app.get("/consensus_client/beacon/get_proposer_slashings", tags=["Consensus Client Beacon Methods"], response_model=ConsensusClientResponseModelGetProposerSlashings)
async def consensus_client_get_proposer_slashings(current_user: User = Depends(get_current_active_user)):
    """
    Retrieves proposer slashings known by the node but not necessarily incorporated into any block
    """
    # TODO: not working yet (empty response)
    response = consensus_client.get_proposer_slashings()
    return response


@ app.get("/consensus_client/beacon/get_voluntary_exits", tags=["Consensus Client Beacon Methods"], response_model=ConsensusClientResponseModelGetVoluntaryExists)
async def consensus_client_get_voluntary_exits(current_user: User = Depends(get_current_active_user)):
    """
    Retrieves voluntary exits known by the node but not necessarily incorporated into any block
    """
    # TODO: not working yet (empty response)
    response = consensus_client.get_voluntary_exits()
    return response


# Consensus Client Config Methods

@ app.get("/consensus_client/config/get_fork_schedule", tags=["Consensus Client Config Methods"], response_model=ConsensusClientResponseModelGetForkSchedule)
async def consensus_client_get_fork_schedule(current_user: User = Depends(get_current_active_user)):
    """
    Retrieve all forks, past present and future, of which this node is aware.
    """
    response = consensus_client.get_fork_schedule()
    return response


@ app.get("/consensus_client/config/get_spec", tags=["Consensus Client Config Methods"], response_model=ConsensusClientResponseModelGetSpec)
async def consensus_client_get_spec(current_user: User = Depends(get_current_active_user)):
    """
    Retrieve specification configuration used on this node. The configuration should include:
    * Constants for all hard forks known by the beacon node, for example the phase 0 and altair values
    * Presets for all hard forks supplied to the beacon node, for example the phase 0 and altair values
    * Configuration for the beacon node, for example the mainnet values

    Values are returned with following format:
    * any value starting with 0x in the spec is returned as a hex string
    * numeric values are returned as a quoted integer
    """
    response = consensus_client.get_spec()
    return response


@ app.get("/consensus_client/config/get_deposit_contract", tags=["Consensus Client Config Methods"], response_model=ConsensusClientResponseModelGetDepositContract)
async def consensus_client_get_deposit_contract(current_user: User = Depends(get_current_active_user)):
    """
    Retrieve Eth1 deposit contract address and chain ID.
    """
    response = consensus_client.get_deposit_contract()
    return response


# Consensus Client Node Methods

@ app.get("/consensus_client/node/get_node_identity", tags=["Consensus Client Node Methods"], response_model=ConsensusClientResponseModelGetNodeIdentity)
async def consensus_client_get_node_identity(current_user: User = Depends(get_current_active_user)):
    """
    Retrieves data about the node's network presence
    """
    response = consensus_client.get_node_identity()
    return response


@ app.get("/consensus_client/node/get_peers", tags=["Consensus Client Node Methods"], response_model=ConsensusClientResponseModelGetPeers)
async def consensus_client_get_peers(current_user: User = Depends(get_current_active_user)):
    """
    Retrieves data about the node's network peers. By default this returns all peers.
    """
    response = consensus_client.get_peers()
    return response


@ app.get("/consensus_client/node/get_peer", tags=["Consensus Client Node Methods"], response_model=ConsensusClientResponseModelGetPeer)
async def consensus_client_get_peer(
        peer_id: str = PEER_ID_QUERY_PARAMETER,
        current_user: User = Depends(get_current_active_user)):
    """
    Retrieves data about the given peer
    """
    response = consensus_client.get_peer(peer_id)
    return response


@ app.get("/consensus_client/node/get_health", tags=["Consensus Client Node Methods"], response_model=ConsensusClientResponseModelGetHealth)
async def consensus_client_get_health(current_user: User = Depends(get_current_active_user)):
    """
    Returns node health status in http status codes. Useful for load balancers.
    """
    response = consensus_client.get_health()
    return response


@ app.get("/consensus_client/node/get_version", tags=["Consensus Client Node Methods"], response_model=ConsensusClientResponseModelGetVersion)
async def consensus_client_get_version(current_user: User = Depends(get_current_active_user)):
    """
    Requests that the beacon node identify information about its implementation in a format similar to a HTTP User-Agent field.
    """
    response = consensus_client.get_version()
    return response


@ app.get("/consensus_client/node/get_syncing", tags=["Consensus Client Node Methods"], response_model=ConsensusClientResponseModelGetSyncing)
async def consensus_client_get_syncing(current_user: User = Depends(get_current_active_user)):
    """
    Requests the beacon node to describe if it's currently syncing or not, and if it is, what block it is up to.
    """
    response = consensus_client.get_syncing()
    return response


# Evaluation

@app.get("/execution_client/evaluation/evaluate_block_request_time", tags=["Evaluation"])
async def execution_client_get_block_request_time(
        block_identifier_list: list[Union[int, str]
                                    ] = BLOCK_IDENTIFIER_LIST_QUERY_PARAMETER,
        full_transactions: bool = FULL_TRANSACTION_QUERY_PARAMETER,
        current_user: User = Depends(get_current_active_user)):
    """
    Evaluate request time of get_block method.

    If full_transactions is True then the 'transactions' key will contain full transactions objects. Otherwise it will be an array of transaction hashes.
    """
    response = evaluation.evaluate_request_time_get_block(
        execution_client, block_identifier_list, full_transactions)

    return response


@app.get("/execution_client/evaluation/evaluate_transaction_request_time", tags=["Evaluation"])
async def execution_client_get_block_request_time(
        transaction_hash_list: list[str] = TRANSACTION_HASH_LIST_QUERY_PARAMETER,
        current_user: User = Depends(get_current_active_user)):
    """
    Evaluate request time of get_transaction method.

    If full_transactions is True then the 'transactions' key will contain full transactions objects. Otherwise it will be an array of transaction hashes.
    """
    response = evaluation.evaluate_request_time_get_transaction(
        execution_client, transaction_hash_list)

    return response


# Other Routes

# catch all unknown routes
@ app.route("/{full_path:path}")
async def catch_all_unknown_routes(full_path: str):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Item not found",
    )
