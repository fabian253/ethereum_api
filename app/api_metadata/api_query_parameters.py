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

UNCLE_INDEX_QUERY_PARAMETER = Query(
    title="Uncle Index",
    description="Index of the uncle",
    example=0
)

CONTRACT_ADDRESS_QUERY_PARAMETER = Query(
    title="Contract Address",
    description="Address of the contract",
    example="0xdAC17F958D2ee523a2206206994597C13D831ec7"
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
