CONTRACT_TABLE = (
    "contract ("
    "contract_address char(42) PRIMARY KEY UNIQUE NOT NULL,"
    "name varchar(200) DEFAULT NULL,"
    "symbol varchar(50) DEFAULT NULL,"
    "block_deployed int DEFAULT NULL,"
    "total_supply varchar(100) DEFAULT NULL,"
    "ERC20 bool NOT NULL DEFAULT FALSE,"
    "ERC20Metadata bool NOT NULL DEFAULT FALSE,"
    "ERC165 bool NOT NULL DEFAULT FALSE,"
    "ERC721 bool NOT NULL DEFAULT FALSE,"
    "ERC721Enumerable bool NOT NULL DEFAULT FALSE,"
    "ERC721Metadata bool NOT NULL DEFAULT FALSE,"
    "ERC777Token bool NOT NULL DEFAULT FALSE,"
    "ERC1155 bool NOT NULL DEFAULT FALSE,"
    "ERC1155TokenReceiver bool NOT NULL DEFAULT FALSE,"
    "abi json DEFAULT NULL"
    ")"
)

TRANSACTION_TABLE = (
    "transaction ("
    "transaction_hash char(66) PRIMARY KEY UNIQUE NOT NULL,"
    "contract_address char(42) NOT NULL,"
    "token_id int DEFAULT NULL,"
    "value varchar(100) DEFAULT NULL,"
    "from_address char(42) NOT NULL,"
    "to_address char(42) NOT NULL,"
    "block_number int NOT NULL"
    ")"
)
