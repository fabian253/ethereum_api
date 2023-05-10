from fastapi import Query

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

FULL_TRANSACTION_QUERY_PARAMETER = Query(
    default=False,
    title="Full Transaction",
    description="Boolean for full transactions"
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
