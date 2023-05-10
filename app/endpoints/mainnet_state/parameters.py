from fastapi import Query

WALLET_ADDRESS_QUERY_PARAMETER = Query(
    title="Wallet address",
    description="Address to check for balance",
    example="0x165CD37b4C644C2921454429E7F9358d18A45e14"
)

BLOCK_IDENTIFIER_OPTIONAL_QUERY_PARAMETER = Query(
    default="latest",
    title="Block identifier",
    description="Integer of a block number or Hash of a block",
    example="latest"
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
