from web3 import Web3
from web3._utils.empty import Empty
from web3.exceptions import BlockNotFound, TransactionNotFound
import json


class ExecutionClientConnector:

    def __init__(self, execution_client_ip: str, execution_client_port: int) -> None:
        self.client_ip = execution_client_ip
        self.client_port = execution_client_port
        # init execution client
        self.execution_client = Web3(Web3.HTTPProvider(
            f"http://{self.client_ip}:{self.client_port}"))

    # Gossip methods

    def block_number(self):
        response = self.execution_client.eth.block_number

        return {"block_number": response}

    # State methods

    def default_account(self):
        response = self.execution_client.eth.default_account

        if type(response) is Empty:
            response = None

        return {"default_account": response}

    def default_block(self):
        response = self.execution_client.eth.default_block

        return {"default_block": response}

    def syncing(self):
        response = self.execution_client.eth.syncing

        if response == False:
            return {"syncing": False}

        return json.loads(Web3.toJSON(response))

    def coinbase(self):
        response = self.execution_client.eth.coinbase

        return {"coinbase": response}

    def mining(self):
        response = self.execution_client.eth.mining

        return {"mining": response}

    def hashrate(self):
        response = self.execution_client.eth.hashrate

        return {"hashrate": response}

    def max_priority_fee(self):
        response = self.execution_client.eth.max_priority_fee

        return {"max_priority_fee": response}

    def accounts(self):
        response = self.execution_client.eth.accounts

        return {"accounts": response}

    def chain_id(self):
        response = self.execution_client.eth.chain_id

        return {"chain_id": response}

    def get_api_version(self):
        response = self.execution_client.api

        return {"api_version": response}

    def get_client_version(self):
        response = self.execution_client.clientVersion

        return {"client_version": response}

    def get_balance(self, wallet_address, block_identifier=None):
        wallet_address = Web3.toChecksumAddress(wallet_address)

        if block_identifier is None:
            response = self.execution_client.eth.get_balance(wallet_address)
        else:
            response = self.execution_client.eth.get_balance(
                wallet_address, block_identifier)

        return {"balance": response}

    def get_block_number(self):
        response = self.execution_client.eth.get_block_number()

        return {"block_number": response}

    def get_storage_at(self, wallet_address, position, block_identifier=None):
        wallet_address = Web3.toChecksumAddress(wallet_address)

        if block_identifier is None:
            response = self.execution_client.eth.get_storage_at(
                wallet_address, position)
        else:
            response = self.execution_client.eth.get_storage_at(
                wallet_address, position, block_identifier)

        return {"storage_value": response}

    def get_code(self, wallet_address):
        wallet_address = Web3.toChecksumAddress(wallet_address)

        response = self.execution_client.eth.get_code(wallet_address)

        return {"bytecode": response}

    def get_transaction_count(self, wallet_address, block_identifier=None):
        wallet_address = Web3.toChecksumAddress(wallet_address)

        if block_identifier is None:
            response = self.execution_client.eth.get_transaction_count(
                wallet_address)
        else:
            response = self.execution_client.eth.get_transaction_count(
                wallet_address, block_identifier)

        return {"transaction_count": response}

    def estimate_gas(self, from_address, to_address, value):
        from_address = Web3.toChecksumAddress(from_address)
        to_address = Web3.toChecksumAddress(to_address)

        response = self.execution_client.eth.estimate_gas({
            "to": to_address,
            "from": from_address,
            "value": value
        })

        return {"gas": response}

    # History methods

    def get_block_transaction_count(self, block_identifier):
        try:
            response = self.execution_client.eth.get_block_transaction_count(
                block_identifier)
        except (BlockNotFound, ValueError):
            return None

        return {"block_transaction_count": response}

    def get_uncle_count(self, block_identifier):
        try:
            response = self.execution_client.eth.get_uncle_count(
                block_identifier)
        except (BlockNotFound, ValueError):
            return None

        return {"uncle_count": response}

    def get_block(self, block_identifier=None, full_transactions=False):
        try:
            if block_identifier is None:
                response = self.execution_client.eth.get_block(
                    self.execution_client.eth.default_block, full_transactions)
            else:
                response = self.execution_client.eth.get_block(
                    block_identifier, full_transactions)
        except (BlockNotFound, ValueError):
            return None

        return json.loads(Web3.toJSON(response))

    def get_transaction(self, transaction_hash: str):
        try:
            response = self.execution_client.eth.get_transaction(
                transaction_hash)
        except TransactionNotFound:
            return None

        return json.loads(Web3.toJSON(response))

    def get_transaction_by_block(self, block_identifier, transaction_index):
        try:
            response = self.execution_client.eth.get_transaction_by_block(
                block_identifier, transaction_index)
        except (TransactionNotFound, ValueError):
            return None

        return json.loads(Web3.toJSON(response))

    def get_transaction_receipt(self, transaction_hash):
        try:
            response = self.execution_client.eth.get_transaction_receipt(
                transaction_hash)
        except (TransactionNotFound, ValueError):
            return None

        return json.loads(Web3.toJSON(response))

    def get_uncle_by_block(self, block_identifier, uncle_index):
        try:
            response = self.execution_client.eth.get_uncle_by_block(
                block_identifier, uncle_index)
        except (BlockNotFound, ValueError):
            return None

        return json.loads(Web3.toJSON(response))
