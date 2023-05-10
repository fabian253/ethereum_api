from fastapi import Query

PEER_ID_QUERY_PARAMETER = Query(
    title="Peer ID",
    description="Peer identifier.",
    example="16Uiu2HAm2m1M9H8JCi9krjdpHBiYDfntNbCgkJ5ha4qh3UsKDskh"
)