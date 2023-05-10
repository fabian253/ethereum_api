API_TITLE = "Ethereum Blockchain API"
API_DESCIPTION = """
API to interact with the Ethereum Blockchain. The focus is on querying data from the blockchain. In addition, a variety of endpoints exist for interacting with smart contracts.

More information about the API can be found on [Github](https://github.com/fabian253/ethereum_api).
"""
API_VERSION = "0.0.1"
API_CONTACT_NAME = "Fabian Galm"
API_CONTACT_EMAIL = "fabian.galm@students.uni-mannheim.de"
API_TAGS_METADATA = [
    {
        "name": "Authentication",
        "description": "Endpoints for authentication and user data retrieval."
    },
    {
        "name": "Mainnet State",
        "description": "Endpoints returning the current state of all data on the Mainnet Blockchain. The state includes account balances, contract data, and gas estimates."
    },
    {
        "name": "Mainnet History",
        "description": "Endpoints to retrieve historical records of each block back to genesis. This includes all block headers, block bodies, uncle blocks, and transaction records."
    },
    {
        "name": "Smart Contract",
        "description": "Endpoints for retrieving data from smart contracts. Additionally, contracts can be interacted with."
    },
    {
        "name": "Beacon Chain",
        "description": "Endpoints allowing data to be queried from the beacon chain."
    },
    {
        "name": "Node State",
        "description": "Endpoints used to query the state of the Ethereum Nodes."
    },
    {
        "name": "Evaluation",
        "description": "Endpoints for performing evaluation."
    }
]
API_SWAGGER_UI_PARAMETERS = {
    "docExpansion": "none"
}
