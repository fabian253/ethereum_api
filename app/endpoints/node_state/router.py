from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import get_current_active_user
from .schemas import *
from .parameters import *
from typing import Union
from app.connectors import execution_client, consensus_client


router = APIRouter(
    prefix="/node",
    tags=["Node State"],
    dependencies=[Depends(get_current_active_user)]
)

execution_client_router = APIRouter(
    prefix="/execution"
)

consensus_client_router = APIRouter(
    prefix="/consensus"
)


@execution_client_router.get("/syncing", response_model=Union[ResponseModelSyncingTrue, ResponseModelSyncingFalse])
async def execution_client_syncing():
    """
    Returns either False if the node is not syncing or a dictionary showing sync status.
    """
    response = execution_client.syncing()
    return response


@execution_client_router.get("/client_version", response_model=ResponseModelClientVersion)
async def execution_client_version():
    """
    Returns the id of the current Ethereum protocol version.
    """
    response = execution_client.get_client_version()
    return response


@execution_client_router.get("/api_version", response_model=ResponseModelApiVersion)
async def api_version():
    """
    Returns the id of the current API version.
    """
    response = execution_client.get_api_version()
    return response


@execution_client_router.get("/mining", response_model=ResponseModelMining)
async def mining():
    """
    Returns boolean as to whether the node is currently mining.
    """
    response = execution_client.mining()
    return response


@execution_client_router.get("/hashrate", response_model=ResponseModelHashrate)
async def hashrate():
    """
    Returns the current number of hashes per second the node is mining with.
    """
    response = execution_client.hashrate()
    return response


@consensus_client_router.get("/syncing", response_model=ResponseModelSyncing)
async def consensus_client_syncing():
    """
    Requests the beacon node to describe if it's currently syncing or not, and if it is, what block it is up to.
    """
    response = consensus_client.get_syncing()
    return response


@consensus_client_router.get("/client_version", response_model=ResponseModelVersion)
async def consensus_client_version():
    """
    Requests that the beacon node identify information about its implementation in a format similar to a HTTP User-Agent field.
    """
    response = consensus_client.get_version()
    return response


@consensus_client_router.get("/health", response_model=ResponseModelHealth)
async def health():
    """
    Returns node health status in http status codes. Useful for load balancers.
    """
    response = consensus_client.get_health()
    return response


@consensus_client_router.get("/node_identity", response_model=ResponseModelNodeIdentity)
async def node_identity():
    """
    Retrieves data about the node's network presence
    """
    response = consensus_client.get_node_identity()
    return response


@consensus_client_router.get("/peers", response_model=ResponseModelPeers)
async def peers():
    """
    Retrieves data about the node's network peers. By default this returns all peers.
    """
    response = consensus_client.get_peers()
    return response


@consensus_client_router.get("/peer", response_model=ResponseModelPeer)
async def peer(
        peer_id: str = PEER_ID_QUERY_PARAMETER):
    """
    Retrieves data about the given peer
    """
    response = consensus_client.get_peer(peer_id)
    return response


@consensus_client_router.get("/fork_schedule", response_model=ResponseModelForkSchedule)
async def fork_schedule():
    """
    Retrieve all forks, past present and future, of which this node is aware.
    """
    response = consensus_client.get_fork_schedule()
    return response


@consensus_client_router.get("/spec", response_model=ResponseModelSpec)
async def spec():
    """
    Retrieve specification configuration used on this node. The configuration should include:
    * Constants for all hard forks known by the beacon node, for example the phase 0 and altair values
    * Presets for all hard forks supplied to the beacon node, for example the phase 0 and altair values
    * Configuration for the beacon node, for example the mainnet values

    Values are returned with following format:
    * any value starting with 0x in the spec is returned as a hex string
    * numeric values are returned as a quoted integer
    """
    response = consensus_client.get_spec()
    return response


@consensus_client_router.get("/deposit_contract", response_model=ResponseModelDepositContract)
async def deposit_contract():
    """
    Retrieve Eth1 deposit contract address and chain ID.
    """
    response = consensus_client.get_deposit_contract()
    return response
