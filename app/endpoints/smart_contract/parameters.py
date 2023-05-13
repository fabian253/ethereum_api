from fastapi import Query

AS_ABI_QUERY_PARAMETER = Query(
    title="As ABI",
    description="Indicate if return should be ABI or names",
    example=True,
    default=True
)

TOKEN_STANDARD_QUERY_PARAMETER = Query(
    title="Token Standard",
    description="Name of Token standard",
    example="ERC20"
)

TOKEN_STANDARD_OPTIONAL_QUERY_PARAMETER = Query(
    title="Token Standard",
    description="Name of Token standard (ERC20, ERC721, ...)",
    example="ERC20",
    default=None
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
    default=None
)

CONTRACT_ADDRESS_QUERY_PARAMETER = Query(
    title="Contract Address independent of token standard",
    description="Address of the contract",
    example="0xdAC17F958D2ee523a2206206994597C13D831ec7"
)
