from fastapi import Query

WALLET_ADDRESS_QUERY_PARAMETER = Query(title="Wallet address", description="Address to check for balance",
                                       example="0x165CD37b4C644C2921454429E7F9358d18A45e14")

BLOCK_IDENTIFIER_QUERY_PARAMETER = Query(default=None, title="Block identifier",
                                         description="Integer of a block number or Hash of a block")

POSITION_QUERY_PARAMETER = Query(
    titel="Position", description="Integer of the position in the storage", example=0)
