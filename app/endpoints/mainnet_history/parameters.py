from fastapi import Query

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

BLOCK_IDENTIFIER_QUERY_PARAMETER = Query(
    title="Block identifier",
    description="Integer of a block number or Hash of a block",
    example="16733081"
)

BLOCK_IDENTIFIER_UNCLE_QUERY_PARAMETER = Query(
    title="Block identifier",
    description="Integer of a block number or Hash of a block",
    example="12237617"
)

BLOCK_IDENTIFIER_OPTIONAL_QUERY_PARAMETER = Query(
    default="latest",
    title="Block identifier",
    description="Integer of a block number or Hash of a block",
    example="latest"
)
