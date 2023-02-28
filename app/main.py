from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from web3.beacon.main import Beacon

import app.config as config
from app.execution_client_connector import ExecutionClientConnector
from app.users_db import users_db

tags_metadata = [
    {
        "name": "Authentication and Users",
        "description": "Endpoints for authentication and user information."
    },
    {
        "name": "Execution Client Gossip Methods",
        "description": "These methods track the head of the chain. This is how transactions make their way around the network, find their way into blocks, and how clients find out about new blocks."
    },
    {
        "name": "Execution Client State Methods",
        "description": "Methods that report the current state of all the data stored. The 'state' is like one big shared piece of RAM, and includes account balances, contract data, and gas estimations."
    },
    {
        "name": "Execution Client History Methods",
        "description": "Fetches historical records of every block back to genesis. This is like one large append-only file, and includes all block headers, block bodies, uncle blocks, and transaction receipts."
    },
    {
        "name": "Consensus Client",
        "description": "Endpoints to retrieve information about the Consensus Client"
    }
]

# execution_client = Web3(Web3.HTTPProvider(
#    f"http://{config.EXECUTION_CLIENT_IP}:{config.EXECUTION_CLIENT_PORT}"))

execution_client = ExecutionClientConnector(
    config.EXECUTION_CLIENT_IP, config.EXECUTION_CLIENT_PORT)

consensus_client = Beacon(
    f"http://{config.CONSENCUS_CLIENT_IP}:{config.CONSENSUS_CLIENT_PORT}")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str


app = FastAPI(
    title="Ethereum Blockchain API",
    description="API to query data from the Ethereum blockchain",
    version="0.0.1",
    contact={
        "name": "Fabian Galm",
        "email": "fabian.galm@students.uni-mannheim.de"
    },
    openapi_tags=tags_metadata
)

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


# Execution Client Gossip methods

@app.get("/execution_client/block_number", tags=["Execution Client Gossip Methods"])
async def execution_client_block_number(current_user: User = Depends(get_current_active_user)):
    response = execution_client.block_number()
    return response


# Execution Client State methods

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


# Execution Client History methods

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


# Consensus Client

@app.get("/consensus_client/get_syncing", tags=["Consensus Client"])
async def get_consensus_client_syncing(current_user: User = Depends(get_current_active_user)):
    response = consensus_client.get_syncing()
    return response["data"]


# Other Routes

# catch all unknown routes
@app.route("/{full_path:path}")
async def catch_all_unknown_routes(full_path: str):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Item not found",
    )
