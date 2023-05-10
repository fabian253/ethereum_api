from fastapi import Query

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
