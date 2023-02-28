from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends, FastAPI, HTTPException, status, Request
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.api_metadata.api_datamodels import *
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
async def overridden_redoc():
    return get_redoc_html(
        openapi_url="/openapi.json",
        title=api_metadata.API_TITLE,
        redoc_favicon_url="/static/favicon.ico"
    )


# Execution Client Gossip Methods

@app.get("/execution_client/block_number", tags=["Execution Client Gossip Methods"])
async def execution_client_block_number(current_user: User = Depends(get_current_active_user)):
    response = execution_client.block_number()
    return response


# Execution Client State Methods

@app.get("/execution_client/default_account", tags=["Execution Client State Methods"])
async def execution_client_default_account(current_user: User = Depends(get_current_active_user)):
    response = execution_client.default_account()
    return response


@app.get("/execution_client/default_block", tags=["Execution Client State Methods"])
async def execution_client_default_block(current_user: User = Depends(get_current_active_user)):
    response = execution_client.default_block()
    return response


@app.get("/execution_client/syncing", tags=["Execution Client State Methods"])
async def execution_client_syncing(current_user: User = Depends(get_current_active_user)):
    response = execution_client.syncing()
    return response


@app.get("/execution_client/mining", tags=["Execution Client State Methods"])
async def execution_client_mining(current_user: User = Depends(get_current_active_user)):
    response = execution_client.mining()
    return response


@app.get("/execution_client/hashrate", tags=["Execution Client State Methods"])
async def execution_client_hashrate(current_user: User = Depends(get_current_active_user)):
    response = execution_client.hashrate()
    return response


@app.get("/execution_client/max_priority_fee", tags=["Execution Client State Methods"])
async def execution_client_max_priority_fee(current_user: User = Depends(get_current_active_user)):
    response = execution_client.max_priority_fee()
    return response


@app.get("/execution_client/accounts", tags=["Execution Client State Methods"])
async def execution_client_accounts(current_user: User = Depends(get_current_active_user)):
    response = execution_client.accounts()
    return response


@app.get("/execution_client/chain_id", tags=["Execution Client State Methods"])
async def execution_client_chain_id(current_user: User = Depends(get_current_active_user)):
    response = execution_client.chain_id()

    return response


@app.get("/execution_client/get_api_version", tags=["Execution Client State Methods"])
async def execution_client_get_api_version(current_user: User = Depends(get_current_active_user)):
    response = execution_client.get_api_version()
    return response


@app.get("/execution_client/get_client_version", tags=["Execution Client State Methods"])
async def execution_client_get_client_version(current_user: User = Depends(get_current_active_user)):
    response = execution_client.get_client_version()
    return response


@app.get("/execution_client/get_balance", tags=["Execution Client State Methods"])
async def execution_client_get_balance(wallet_address: str, block_identifier: Union[int, None] = None, current_user: User = Depends(get_current_active_user)):
    response = execution_client.get_balance(wallet_address, block_identifier)
    return response


@app.get("/execution_client/get_block_number", tags=["Execution Client State Methods"])
async def execution_client_get_block_number(current_user: User = Depends(get_current_active_user)):
    response = execution_client.get_block_number()
    return response


@app.get("/execution_client/get_storage_at", tags=["Execution Client State Methods"])
async def execution_client_get_storage_at(wallet_address: str, position: int, block_identifier: Union[int, None] = None, current_user: User = Depends(get_current_active_user)):
    response = execution_client.get_storage_at(
        wallet_address, position, block_identifier)
    return response


@app.get("/execution_client/get_code", tags=["Execution Client State Methods"])
async def execution_client_get_code(wallet_address: str, current_user: User = Depends(get_current_active_user)):
    response = execution_client.get_code(wallet_address)
    return response


@app.get("/execution_client/get_transaction_count", tags=["Execution Client State Methods"])
async def execution_client_get_transaction_count(wallet_address: str, block_identifier: Union[int, None] = None, current_user: User = Depends(get_current_active_user)):
    reponse = execution_client.get_transaction_count(
        wallet_address, block_identifier)
    return reponse


@app.get("/execution_client/estimate_gas", tags=["Execution Client State Methods"])
async def execution_client_estimate_gas(from_addrress: str, to_address: str, value: int,  current_user: User = Depends(get_current_active_user)):
    response = execution_client.estimate_gas(from_addrress, to_address, value)
    return response


# Execution Client History Methods

@app.get("/execution_client/get_block_transaction_count", tags=["Execution Client History Methods"])
async def execution_client_get_block_transaction_count(block_identifier: Union[int, str], current_user: User = Depends(get_current_active_user)):
    response = execution_client.get_block_transaction_count(block_identifier)
    return response


@app.get("/execution_client/get_uncle_count", tags=["Execution Client History Methods"])
async def execution_client_get_uncle_count(block_identifier: Union[int, str], current_user: User = Depends(get_current_active_user)):
    response = execution_client.get_uncle_count(block_identifier)

    if response is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Block not found (block_identifier: {block_identifier})"
        )

    return response


@app.get("/execution_client/get_block", tags=["Execution Client History Methods"])
async def execution_client_get_block(block_identifier: Union[int, str, None] = None, full_transactions: bool = False,  current_user: User = Depends(get_current_active_user)):
    response = execution_client.get_block(block_identifier, full_transactions)

    if response is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Block not found (block_identifier: {block_identifier})"
        )

    return response


@app.get("/execution_client/get_transaction_by_block", tags=["Execution Client History Methods"])
async def execution_client_get_transaction_by_block(block_identifier: Union[int, str], transaction_index: int, current_user: User = Depends(get_current_active_user)):
    response = execution_client.get_transaction_by_block(
        block_identifier, transaction_index)

    if response is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Transaction not found (block_identifier: {block_identifier}, transaction_index: {transaction_index})"
        )

    return response


@app.get("/execution_client/get_transaction_receipt", tags=["Execution Client History Methods"])
async def execution_client_get_transaction_receipt(transaction_hash: str, current_user: User = Depends(get_current_active_user)):
    response = execution_client.get_transaction_receipt(transaction_hash)
    return response


@app.get("/execution_client/get_uncle_by_block", tags=["Execution Client History Methods"])
async def execution_client_get_uncle_by_block(block_identifier: Union[int, str], uncle_index: int, current_user: User = Depends(get_current_active_user)):
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
async def consensus_client_get_hash_root(state_id: str = "head", current_user: User = Depends(get_current_active_user)):
    response = consensus_client.get_hash_root(state_id)
    return response


@app.get("/consensus_client/get_fork_data", tags=["Consensus Client Beacon Methods"])
async def consensus_client_get_fork_data(state_id: str = "head", current_user: User = Depends(get_current_active_user)):
    response = consensus_client.get_fork_data(state_id)
    return response


@app.get("/consensus_client/get_finality_checkpoint", tags=["Consensus Client Beacon Methods"])
async def consensus_client_get_finality_checkpoint(state_id: str = "head", current_user: User = Depends(get_current_active_user)):
    response = consensus_client.get_finality_checkpoint(state_id)
    return response

# TODO: not working


@app.get("/consensus_client/get_validators", tags=["Consensus Client Beacon Methods"])
async def consensus_client_get_validators(state_id: str = "head", current_user: User = Depends(get_current_active_user)):
    response = consensus_client.get_validators(state_id)
    return response


@app.get("/consensus_client/get_validator", tags=["Consensus Client Beacon Methods"])
async def consensus_client_get_validator(validator_id: int, state_id: str = "head", current_user: User = Depends(get_current_active_user)):
    response = consensus_client.get_validator(validator_id, state_id)
    return response


@app.get("/consensus_client/get_validator_balances", tags=["Consensus Client Beacon Methods"])
async def consensus_client_get_validator_balances(state_id: str = "head", current_user: User = Depends(get_current_active_user)):
    response = consensus_client.get_validator_balances(state_id)
    return response


@app.get("/consensus_client/get_epoch_committees", tags=["Consensus Client Beacon Methods"])
async def consensus_client_get_epoch_committees(state_id: str = "head", current_user: User = Depends(get_current_active_user)):
    response = consensus_client.get_epoch_committees(state_id)
    return response


@app.get("/consensus_client/get_block_headers", tags=["Consensus Client Beacon Methods"])
async def consensus_client_get_block_headers(current_user: User = Depends(get_current_active_user)):
    response = consensus_client.get_block_headers()
    return response


@app.get("/consensus_client/get_block_header", tags=["Consensus Client Beacon Methods"])
async def consensus_client_get_block_header(block_id: int, current_user: User = Depends(get_current_active_user)):
    response = consensus_client.get_block_header(block_id)
    return response


@app.get("/consensus_client/get_block", tags=["Consensus Client Beacon Methods"])
async def consensus_client_get_block(block_id: int, current_user: User = Depends(get_current_active_user)):
    response = consensus_client.get_block(block_id)
    return response


@app.get("/consensus_client/get_block_root", tags=["Consensus Client Beacon Methods"])
async def consensus_client_get_block_root(block_id: int, current_user: User = Depends(get_current_active_user)):
    response = consensus_client.get_block_root(block_id)
    return response


@app.get("/consensus_client/get_block_attestations", tags=["Consensus Client Beacon Methods"])
async def consensus_client_get_block_attestations(block_id: int, current_user: User = Depends(get_current_active_user)):
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
async def consensus_client_get_peer(peer_id: str, current_user: User = Depends(get_current_active_user)):
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
