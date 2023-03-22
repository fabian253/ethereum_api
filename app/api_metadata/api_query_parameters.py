from fastapi import Query


# Execution Client

WALLET_ADDRESS_QUERY_PARAMETER = Query(
    title="Wallet address",
    description="Address to check for balance",
    example="0x165CD37b4C644C2921454429E7F9358d18A45e14"
)

BLOCK_IDENTIFIER_QUERY_PARAMETER = Query(
    title="Block identifier",
    description="Integer of a block number or Hash of a block",
    example="16733081"
)

BLOCK_IDENTIFIER_LIST_QUERY_PARAMETER = Query(
    title="Block identifier list",
    description="List of Integer of a block number or Hash of a block",
    example=[6395765,
             11237854,
             8714247,
             6134458,
             3349559,
             9828143,
             9433957,
             12212426,
             5701598,
             3875276]
)

BLOCK_IDENTIFIER_OPTIONAL_QUERY_PARAMETER = Query(
    default="latest",
    title="Block identifier",
    description="Integer of a block number or Hash of a block",
    example="latest"
)

BLOCK_IDENTIFIER_UNCLE_QUERY_PARAMETER = Query(
    title="Block identifier",
    description="Integer of a block number or Hash of a block",
    example="12237617"
)

POSITION_QUERY_PARAMETER = Query(
    titel="Position",
    description="Integer of the position in the storage",
    example=0
)

FROM_ADDRESS_QUERY_PARAMETER = Query(
    title="From Address",
    description="Address to send the transaction from",
    example="0xd57db5c31a5185c238448a210f15135ebb8b0574"
)

TO_ADDRESS_QUERY_PARAMETER = Query(
    title="To Address",
    description="Address to send the transaction to",
    example="0x6c6e21ff463f406745b665322c7157b1d7c0ac6b"
)

TRANSACTION_VALUE_QUERY_PARAMETER = Query(
    title="Value",
    description="Transaction value",
    example=1
)

FULL_TRANSACTION_QUERY_PARAMETER = Query(
    default=False,
    title="Full Transaction",
    description="Boolean for full transactions"
)

TRANSACTION_INDEX_QUERY_PARAMETER = Query(
    title="Transaction Index",
    description="Index of the transaction in the block",
    example=0
)

TRANSACTION_HASH_QUERY_PARAMETER = Query(
    title="Transaction Hash",
    description="Hash of the transaction",
    example="0xb65321793b9d0c2e6f4005b0d9427229dcf85c551c8506799415df35800f7b8d"
)


TRANSACTION_HASH_LIST_QUERY_PARAMETER = Query(
    title="Transaction Hash list",
    description="List of Hash of the transaction",
    example=[
        "0xe6e0b70bfceaf1cf4d2b43931937b25d8e388543f3950be1045e93d7968fef11",
        "0xf6e0235cb63cae6b59da017397516cf4db33f151f906f07a99f05d88b49aedaa",
        "0x1b649d03a932e4b63a9fbaec3769fc5d1a19f371aa7dcf9ef307463c3fa346c8",
        "0xa88421d537992710b97816e8157735511b13876cdec4424748ba0d3231b83dee",
        "0x99e26f76fe29bcd4ada237403eafddf6d29f5e51279a66c6c6ac04a78d5c0cc8",
        "0x2a47b8b1ba2bd97ff6339939fa085a066b54b937e1011308991b911506710ff3",
        "0xab0cb6beab255331efe34b1d4ce01ccae6cecd9af2aac66bf33185c305f638e5",
        "0xd75de866e904cf70419c8becbcb35227d7678db8b6c7b5fd4aaffe0a83abfe3b",
        "0x88969a6b9bdaa3ae094c18ee435110d52c1f5f71be8878797423e85899d57f5b",
        "0x290930b9fe4309c3470b17303fdefe426f0676c989e72f97704fce182f82374d"
    ]
)

UNCLE_INDEX_QUERY_PARAMETER = Query(
    title="Uncle Index",
    description="Index of the uncle",
    example=0
)


CONTRACT_ADDRESS_QUERY_PARAMETER = Query(
    title="Contract Address independent of token standard",
    description="Address of the contract",
    example="0xdAC17F958D2ee523a2206206994597C13D831ec7"
)

AS_ABI_QUERY_PARAMETER = Query(
    title="As ABI",
    description="Indicate if return should be ABI or names",
    example=True,
    default=True
)

TOKEN_ID_QUERY_PARAMETER = Query(
    title="Token ID",
    description="ID of the token",
    example=0
)

TOKEN_STANDARD_QUERY_PARAMETER = Query(
    title="Token Standard",
    description="Name of Token standard",
    example="ERC20"
)

CONTRACT_FUNCTION_QUERY_PARAMETER = Query(
    title="Function Name",
    description="Name of the contract function",
    example="name"
)

CONTRACT_FUNCTION_ARGS_QUERY_PARAMETER = Query(
    title="Function Args",
    description="Arguments of the contract function",
    default=[]
)

TOKEN_TRANSFERS_FROM_BLOCK_QUERY_PARAMETER = Query(
    title="From Block",
    description="From block as int, hex or 'latest'",
    default=0
)

TOKEN_TRANSFERS_TO_BLOCK_QUERY_PARAMETER = Query(
    title="To Block",
    description="To block as int, hex or 'latest'",
    default="latest"
)

ERC721_TOKEN_TRANSFERS_CONTRACT_ADDRESS_QUERY_PARAMETER = Query(
    title="Contract Address",
    description="Contract address of the ERC721 contract",
    example="0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D"
)

ERC721_TOKEN_TRANSFERS_FROM_ADDRESS_QUERY_PARAMETER = Query(
    title="From Address",
    description="From Address",
    example="0xDAFCe4AcC2703A24F29d1321AdAADF5768F54642",
    default=None
)

ERC721_TOKEN_TRANSFERS_TO_ADDRESS_QUERY_PARAMETER = Query(
    title="To Address",
    description="To Address",
    example="0xDBfD76AF2157Dc15eE4e57F3f942bB45Ba84aF24",
    default=None
)

ERC721_TOKEN_TRANSFERS_TOKEN_ID_QUERY_PARAMETER = Query(
    title="Token ID",
    description="Token ID",
    example=8240,
    default=None
)

ERC20_TOKEN_TRANSFERS_CONTRACT_ADDRESS_QUERY_PARAMETER = Query(
    title="Contract Address",
    description="Contract address of the ERC20 contract",
    example="0xdAC17F958D2ee523a2206206994597C13D831ec7"
)

ERC20_TOKEN_TRANSFERS_FROM_ADDRESS_QUERY_PARAMETER = Query(
    title="From Address",
    description="From Address",
    example="0xD7FCb3C89Ac0d60f49d5923Fb778dbcc65C40D90",
    default=None
)

ERC20_TOKEN_TRANSFERS_TO_ADDRESS_QUERY_PARAMETER = Query(
    title="To Address",
    description="To Address",
    example="0xBd9B34cCbb8db0FDECb532B1EAF5D46f5b673fE8",
    default=None
)

ERC20_TOKEN_TRANSFERS_VALUE_QUERY_PARAMETER = Query(
    title="Value",
    description="Value of transfer",
    example=1,
    default=None
)


# Consensus Client

STATE_ID_QUERY_PARAMETER = Query(
    title="State ID",
    description='State identifier. Can be one of: "head" (canonical head in node\'s view), "genesis", "finalized", "justified", <slot>, <hex encoded stateRoot with 0x prefix>.',
    example="head"
)

VALIDATOR_ID_QUERY_PARAMETER = Query(
    title="Validator ID",
    description="Either hex encoded public key (any bytes48 with 0x prefix) or validator index",
    example=0
)

BLOCK_ID_QUERY_PARAMETER = Query(
    title="Block ID",
    description='Block identifier. Can be one of: "head" (canonical head in node\'s view), "genesis", "finalized", <slot>, <hex encoded blockRoot with 0x prefix>.',
    example="head"
)

PEER_ID_QUERY_PARAMETER = Query(
    title="Peer ID",
    description="Peer identifier.",
    example="16Uiu2HAm2m1M9H8JCi9krjdpHBiYDfntNbCgkJ5ha4qh3UsKDskh"
)
