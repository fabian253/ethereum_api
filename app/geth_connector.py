from web3 import Web3
import json
from web3.contract import Contract


class GethConnector:

    def __init__(self, geth_node_http_host) -> None:
        self.w3_connection = Web3(Web3.HTTPProvider(geth_node_http_host))

    def get_latest_block_number(self):
        latest_block_number = self.w3_connection.eth.get_block_number()

        return latest_block_number

    def get_latest_block(self) -> dict:
        latest_block = self.w3_connection.eth.get_block('latest')

        return json.loads(Web3.toJSON(latest_block))

    def get_block(self, block_number):
        block = self.w3_connection.eth.get_block(block_number, True)

        return json.loads(Web3.toJSON(block))

    def get_contract(self, contract_address: str, abi: dict) -> Contract:
        contract = self.w3_connection.eth.contract(
            address=contract_address, abi=abi)

        return contract

    def get_transactions_by_wallet_address(self, wallet_address, from_block, to_block):
        wallet_transactions = []

        for block_number in range(from_block, to_block):
            block = self.get_block(block_number)

            for transaction in block["transactions"]:
                
                if transaction["from"] == wallet_address or transaction["to"] == wallet_address:
                    wallet_transactions.append(transaction)

        return wallet_transactions
