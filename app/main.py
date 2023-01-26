from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from web3 import Web3
from web3.beacon.main import Beacon

import app.config as config
from app.execution_client_connector import ExecutionClientConnector
from app.user_db import users_db

tags_metadata = [
    {
        "name": "Authentication and Users",
        "description": "Endpoints for authentication and user information"
    },
    {
        "name": "Block data",
        "description": "Endpoints to query data from the blocks of the blockchain"
    },
    {
        "name": "Execution Client Information",
        "description": "Endpoints to retrieve information about the Execution Client"
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


@app.get("/get_block", tags=["Block data"])
async def get_block(current_user: User = Depends(get_current_active_user), block_number: int = -1):
    if block_number != -1:
        response = execution_client.get_block(block_number)
    else:
        response = execution_client.get_block()

    return response


@app.get("/get_syncing", tags=["Execution Client Information"])
async def get_syncing(current_user: User = Depends(get_current_active_user)):
    response = consensus_client.get_syncing()

    return response["data"]
