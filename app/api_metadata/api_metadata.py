API_TITLE = "Ethereum Blockchain API"
API_DESCIPTION = """
API to query data from the Ethereum blockchain
"""
API_VERSION = "0.0.1"
API_CONTACT_NAME = "Fabian Galm"
API_CONTACT_EMAIL = "fabian.galm@students.uni-mannheim.de"
API_TAGS_METADATA = [
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
        "name": "Consensus Client Beacon Methods",
        "description": "Set of endpoints to query beacon chain."
    },
    {
        "name": "Consensus Client Config Methods",
        "description": "Endpoints to query chain configuration, specification, and fork schedules."
    },
    {
        "name": "Consensus Client Node Methods",
        "description": "Endpoints to query node related informations"
    }
]
API_SWAGGER_UI_PARAMETERS = {
    "docExpansion": "none"
}
