from fastapi import FastAPI
import app.config as config
from web3 import Web3
from web3.beacon import Beacon
from app.execution_client_connector import ExecutionClientConnector
import json

app = FastAPI()

#execution_client = Web3(Web3.HTTPProvider(
#    f"http://{config.EXECUTION_CLIENT_IP}:{config.EXECUTION_CLIENT_PORT}"))

execution_client = ExecutionClientConnector(
    config.EXECUTION_CLIENT_IP, config.EXECUTION_CLIENT_PORT)

consensus_client = Beacon(
    f"http://{config.CONSENCUS_CLIENT_IP}:{config.CONSENSUS_CLIENT_PORT}")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/get_block")
async def get_block(block_number: int = None):
    if block_number is not None:
        response = execution_client.get_block(block_number)
    else:
        response = execution_client.get_block()

    return response


@app.get("/get_syncing")
async def get_syncing():
    response = consensus_client.get_syncing()

    return response["data"]
