from web3 import Web3
from web3.exceptions import BlockNotFound, TransactionNotFound
import json


class ExecutionClientConnector:

    def __init__(self, execution_client_ip: str, execution_client_port: int) -> None:
        self.client_ip = execution_client_ip
        self.client_port = execution_client_port
        # init execution client
        self.execution_client = Web3(Web3.HTTPProvider(
            f"http://{self.client_ip}:{self.client_port}"))

    # Web3 API Properties

    def get_api_version(self):
        response = self.execution_client.api

        return {"api_version": response}

    def get_client_version(self):
        response = self.execution_client.clientVersion

        return {"client_version": response}

    def get_syncing(self):
        response = self.get_syncing()

        return json.loads(Web3.toJSON(response))

    # Web3 Eth API Properties

    def get_default_account(self):
        response = self.execution_client.eth.default_account

        print(type(response))

        print(response)

        return {"default_account": response}

    def get_default_block(self):
        response = self.execution_client.eth.default_block

        return {"default_block": response}

    def get_syncing(self):
        response = self.execution_client.eth.syncing

        return json.loads(Web3.toJSON(response))

    def get_block_number(self):
        response = self.execution_client.eth.block_number

        return {"block_number": response}

    # Web3 Eth API Methods

    def get_block(self, block_number: int = None):
        try:
            if block_number is not None:
                response = self.execution_client.eth.get_block(block_number)
            else:
                response = self.execution_client.eth.get_block("latest")
        except BlockNotFound:
            return None

        return json.loads(Web3.toJSON(response))

    def get_transaction(self, transaction_hash: str):
        try:
            response = self.execution_client.eth.get_transaction(
                transaction_hash)
        except TransactionNotFound:
            return None

        return json.loads(Web3.toJSON(response))
