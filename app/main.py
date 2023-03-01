from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends, FastAPI, HTTPException, status, Request, Query
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
from app.execution_client_connector import ExecutionClientConnector
from app.consensus_client_connector import ConsensusClientConnector
from app.users_db import users_db


execution_client = ExecutionClientConnector(
    config.EXECUTION_CLIENT_IP, config.EXECUTION_CLIENT_PORT)

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

@app.get("/execution_client/block_number", tags=["Execution Client Gossip Methods"], response_model=ExecutionClientResponseModelBlockNumber)
async def execution_client_block_number(current_user: User = Depends(get_current_active_user)):
    """
    Returns the number of most recent block.
    """
    response = execution_client.block_number()
    return response


# Execution Client State Methods

@app.get("/execution_client/default_account", tags=["Execution Client State Methods"], response_model=ExecutionClientResponseModelDefaultAccount)
async def execution_client_default_account(current_user: User = Depends(get_current_active_user)):
    """
    Returns the ethereum address that will be used as the default from address for all transactions. 

    Defaults to empty.
    """
    response = execution_client.default_account()
    return response


@app.get("/execution_client/default_block", tags=["Execution Client State Methods"], response_model=ExecutionClientResponseModelDefaultBlock)
async def execution_client_default_block(current_user: User = Depends(get_current_active_user)):
    """
    Returns the default block number that will be used for any RPC methods that accept a block identifier. 

    Defaults to 'latest'.
    """
    response = execution_client.default_block()
    return response


@app.get("/execution_client/syncing", tags=["Execution Client State Methods"], response_model=ExecutionClientResponseModelSyncing)
async def execution_client_syncing(current_user: User = Depends(get_current_active_user)):
    """
    Returns either False if the node is not syncing or a dictionary showing sync status.
    """
    # TODO: include second response model if node is not syncing
    response = execution_client.syncing()
    return response


@app.get("/execution_client/mining", tags=["Execution Client State Methods"], response_model=ExecutionClientResponseModelMining)
async def execution_client_mining(current_user: User = Depends(get_current_active_user)):
    """
    Returns boolean as to whether the node is currently mining.
    """
    response = execution_client.mining()
    return response


@app.get("/execution_client/hashrate", tags=["Execution Client State Methods"], response_model=ExecutionClientResponseModelHashrate)
async def execution_client_hashrate(current_user: User = Depends(get_current_active_user)):
    """
    Returns the current number of hashes per second the node is mining with.
    """
    response = execution_client.hashrate()
    return response


@app.get("/execution_client/max_priority_fee", tags=["Execution Client State Methods"], response_model=ExecutionClientResponseModelMaxPriorityFee)
async def execution_client_max_priority_fee(current_user: User = Depends(get_current_active_user)):
    """
    Returns a suggestion for a max priority fee for dynamic fee transactions in Wei.
    """
    response = execution_client.max_priority_fee()
    return response


@app.get("/execution_client/accounts", tags=["Execution Client State Methods"], response_model=ExecutionClientResponseModelAccounts)
async def execution_client_accounts(current_user: User = Depends(get_current_active_user)):
    """
    Returns the list of known accounts.
    """
    response = execution_client.accounts()
    return response


@app.get("/execution_client/chain_id", tags=["Execution Client State Methods"], response_model=ExecutionClientResponseModelChainId)
async def execution_client_chain_id(current_user: User = Depends(get_current_active_user)):
    """
    Returns an integer value for the currently configured “Chain Id” value introduced in EIP-155.

    Returns None if no Chain Id is available.
    """
    # TODO: add None into response model
    response = execution_client.chain_id()

    return response


@app.get("/execution_client/get_api_version", tags=["Execution Client State Methods"], response_model=ExecutionClientResponseModelGetApiVersion)
async def execution_client_get_api_version(current_user: User = Depends(get_current_active_user)):
    """
    Returns the id of the current API version.
    """
    response = execution_client.get_api_version()
    return response


@app.get("/execution_client/get_client_version", tags=["Execution Client State Methods"], response_model=ExecutionClientResponseModelGetClientVersion)
async def execution_client_get_client_version(current_user: User = Depends(get_current_active_user)):
    """
    Returns the id of the current Ethereum protocol version.
    """
    response = execution_client.get_client_version()
    return response


@app.get("/execution_client/get_balance", tags=["Execution Client State Methods"], response_model=ExecutionClientResponseModelGetBalance)
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


@app.get("/execution_client/get_block_number", tags=["Execution Client State Methods"], response_model=ExecutionClientResponseModelGetBlockNumber)
async def execution_client_get_block_number(current_user: User = Depends(get_current_active_user)):
    """
    Returns the number of the most recent block.
    """
    response = execution_client.get_block_number()
    return response


@app.get("/execution_client/get_storage_at", tags=["Execution Client State Methods"], response_model=ExecutionClientResponseModelGetStorageAt)
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


@app.get("/execution_client/get_code", tags=["Execution Client State Methods"], response_model=ExecutionClientResponseModelGetCode)
async def execution_client_get_code(
        wallet_address: str = WALLET_ADDRESS_QUERY_PARAMETER,
        current_user: User = Depends(get_current_active_user)):
    """
    Returns the bytecode for the given wallet_address at the block specified by block_identifier.

    wallet_address may be a checksum address or an ENS name    
    """
    response = execution_client.get_code(wallet_address)
    return response


@app.get("/execution_client/get_transaction_count", tags=["Execution Client State Methods"], response_model=ExecutionClientResponseModelGetTransactionCount)
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


@app.get("/execution_client/estimate_gas", tags=["Execution Client State Methods"], response_model=ExecutionClientResponseModelEstimateGas)
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

@app.get("/execution_client/get_block_transaction_count", tags=["Execution Client History Methods"], response_model=ExecutionClientResponseModelGetBlockTransactionCount)
async def execution_client_get_block_transaction_count(
        block_identifier: Union[int, str] = BLOCK_IDENTIFIER_QUERY_PARAMETER,
        current_user: User = Depends(get_current_active_user)):
    """
    Returns the number of transactions in the block specified by block_identifier. 
    Delegates to eth_getBlockTransactionCountByNumber if block_identifier is an integer or one of the predefined block parameters 'latest', 'earliest', 'pending', 'safe', 'finalized', otherwise delegates to eth_getBlockTransactionCountByHash. 

    Throws BlockNotFoundError if transactions are not found.
    """
    # TODO: add error for block not found
    response = execution_client.get_block_transaction_count(block_identifier)
    return response


@app.get("/execution_client/get_uncle_count", tags=["Execution Client History Methods"], response_model=ExecutionClientResponseModelGetUncleCount)
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


@app.get("/execution_client/get_block", tags=["Execution Client History Methods"], response_model=Union[ExecutionClientResponseModelGetBlockFalse, ExecutionClientResponseModelGetBlockTrue])
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

    print(response)

    if response is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Block not found (block_identifier: {block_identifier})"
        )

    return response


@app.get("/execution_client/get_transaction_by_block", tags=["Execution Client History Methods"], response_model=ExecutionClientResponseModelGetTransactionByBlock)
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


@app.get("/execution_client/get_transaction_receipt", tags=["Execution Client History Methods"], response_model=ExecutionClientResponseModelGetTransactionReceipt)
async def execution_client_get_transaction_receipt(
        transaction_hash: str = TRANSACTION_HASH_QUERY_PARAMETER,
        current_user: User = Depends(get_current_active_user)):
    """
    Returns the transaction receipt specified by transaction_hash. 

    Throws TransactionNotFound if a transaction cannot be found.

    If status in response equals 1 the transaction was successful. If it is equals 0 the transaction was reverted by EVM.
    """
    # TODO: Add exception
    response = execution_client.get_transaction_receipt(transaction_hash)
    return response


@app.get("/execution_client/get_uncle_by_block", tags=["Execution Client History Methods"], response_model=ExecutionClientResponseModelGetUncleByBlock)
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


# Consensus Client Beacon Methods

@app.get("/consensus_client/get_genesis", tags=["Consensus Client Beacon Methods"])
async def consensus_client_get_genesis(current_user: User = Depends(get_current_active_user)):
    response = consensus_client.get_genesis()
    return response


@app.get("/consensus_client/get_hash_root", tags=["Consensus Client Beacon Methods"])
async def consensus_client_get_hash_root(
        state_id: str = "head",
        current_user: User = Depends(get_current_active_user)):
    response = consensus_client.get_hash_root(state_id)
    return response


@app.get("/consensus_client/get_fork_data", tags=["Consensus Client Beacon Methods"])
async def consensus_client_get_fork_data(
        state_id: str = "head",
        current_user: User = Depends(get_current_active_user)):
    response = consensus_client.get_fork_data(state_id)
    return response


@app.get("/consensus_client/get_finality_checkpoint", tags=["Consensus Client Beacon Methods"])
async def consensus_client_get_finality_checkpoint(
        state_id: str = "head",
        current_user: User = Depends(get_current_active_user)):
    response = consensus_client.get_finality_checkpoint(state_id)
    return response


@app.get("/consensus_client/get_validators", tags=["Consensus Client Beacon Methods"])
async def consensus_client_get_validators(
        state_id: str = "head",
        current_user: User = Depends(get_current_active_user)):
    # TODO: not working
    response = consensus_client.get_validators(state_id)
    return response


@app.get("/consensus_client/get_validator", tags=["Consensus Client Beacon Methods"])
async def consensus_client_get_validator(
        validator_id: int,
        state_id: str = "head",
        current_user: User = Depends(get_current_active_user)):
    response = consensus_client.get_validator(validator_id, state_id)
    return response


@app.get("/consensus_client/get_validator_balances", tags=["Consensus Client Beacon Methods"])
async def consensus_client_get_validator_balances(
        state_id: str = "head",
        current_user: User = Depends(get_current_active_user)):
    response = consensus_client.get_validator_balances(state_id)
    return response


@app.get("/consensus_client/get_epoch_committees", tags=["Consensus Client Beacon Methods"])
async def consensus_client_get_epoch_committees(
        state_id: str = "head",
        current_user: User = Depends(get_current_active_user)):
    response = consensus_client.get_epoch_committees(state_id)
    return response


@app.get("/consensus_client/get_block_headers", tags=["Consensus Client Beacon Methods"])
async def consensus_client_get_block_headers(current_user: User = Depends(get_current_active_user)):
    response = consensus_client.get_block_headers()
    return response


@app.get("/consensus_client/get_block_header", tags=["Consensus Client Beacon Methods"])
async def consensus_client_get_block_header(
        block_id: int,
        current_user: User = Depends(get_current_active_user)):
    response = consensus_client.get_block_header(block_id)
    return response


@app.get("/consensus_client/get_block", tags=["Consensus Client Beacon Methods"])
async def consensus_client_get_block(
        block_id: int,
        current_user: User = Depends(get_current_active_user)):
    response = consensus_client.get_block(block_id)
    return response


@app.get("/consensus_client/get_block_root", tags=["Consensus Client Beacon Methods"])
async def consensus_client_get_block_root(
        block_id: int,
        current_user: User = Depends(get_current_active_user)):
    response = consensus_client.get_block_root(block_id)
    return response


@app.get("/consensus_client/get_block_attestations", tags=["Consensus Client Beacon Methods"])
async def consensus_client_get_block_attestations(
        block_id: int,
        current_user: User = Depends(get_current_active_user)):
    response = consensus_client.get_block_attestations(block_id)
    return response


@app.get("/consensus_client/get_attestations", tags=["Consensus Client Beacon Methods"])
async def consensus_client_get_attestations(current_user: User = Depends(get_current_active_user)):
    response = consensus_client.get_attestations()
    return response


@app.get("/consensus_client/get_attester_slashings", tags=["Consensus Client Beacon Methods"])
async def consensus_client_get_attester_slashings(current_user: User = Depends(get_current_active_user)):
    response = consensus_client.get_attester_slashings()
    return response


@app.get("/consensus_client/get_proposer_slashings", tags=["Consensus Client Beacon Methods"])
async def consensus_client_get_proposer_slashings(current_user: User = Depends(get_current_active_user)):
    response = consensus_client.get_proposer_slashings()
    return response


@app.get("/consensus_client/get_voluntary_exits", tags=["Consensus Client Beacon Methods"])
async def consensus_client_get_voluntary_exits(current_user: User = Depends(get_current_active_user)):
    response = consensus_client.get_voluntary_exits()
    return response


# Consensus Client Config Methods

@app.get("/consensus_client/get_fork_schedule", tags=["Consensus Client Config Methods"])
async def consensus_client_get_fork_schedule(current_user: User = Depends(get_current_active_user)):
    response = consensus_client.get_fork_schedule()
    return response


@app.get("/consensus_client/get_spec", tags=["Consensus Client Config Methods"])
async def consensus_client_get_spec(current_user: User = Depends(get_current_active_user)):
    response = consensus_client.get_spec()
    return response


@app.get("/consensus_client/get_deposit_contract", tags=["Consensus Client Config Methods"])
async def consensus_client_get_deposit_contract(current_user: User = Depends(get_current_active_user)):
    response = consensus_client.get_deposit_contract()
    return response


# Consensus Client Node Methods

@app.get("/consensus_client/get_node_identity", tags=["Consensus Client Node Methods"])
async def consensus_client_get_node_identity(current_user: User = Depends(get_current_active_user)):
    response = consensus_client.get_node_identity()
    return response


@app.get("/consensus_client/get_peers", tags=["Consensus Client Node Methods"])
async def consensus_client_get_peers(current_user: User = Depends(get_current_active_user)):
    response = consensus_client.get_peers()
    return response


@app.get("/consensus_client/get_peer", tags=["Consensus Client Node Methods"])
async def consensus_client_get_peer(
        peer_id: str,
        current_user: User = Depends(get_current_active_user)):
    response = consensus_client.get_peer(peer_id)
    return response


@app.get("/consensus_client/get_health", tags=["Consensus Client Node Methods"])
async def consensus_client_get_health(current_user: User = Depends(get_current_active_user)):
    response = consensus_client.get_health()
    return response


@app.get("/consensus_client/get_version", tags=["Consensus Client Node Methods"])
async def consensus_client_get_version(current_user: User = Depends(get_current_active_user)):
    response = consensus_client.get_version()
    return response


@app.get("/consensus_client/get_syncing", tags=["Consensus Client Node Methods"])
async def consensus_client_get_syncing(current_user: User = Depends(get_current_active_user)):
    response = consensus_client.get_syncing()
    return response


# Other Routes

# catch all unknown routes
@app.route("/{full_path:path}")
async def catch_all_unknown_routes(full_path: str):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Item not found",
    )
