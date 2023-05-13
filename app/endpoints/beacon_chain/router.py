from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import get_current_active_user
from .schemas import *
from .parameters import *
from typing import Union
from app.connectors import consensus_client
from app.api_params.api_decorators import *

router = APIRouter(
    prefix="/beacon",
    tags=["Beacon Chain"],
    dependencies=[Depends(get_current_active_user)]
)


@router.get("/genesis", responses={200: {"model": ResponseModelGenesis}, 503: {"model": ErrorResponseModel}})
@connection_decorator
async def genesis():
    """
    Retrieve details of the chain's genesis which can be used to identify chain.
    """
    response = consensus_client.get_genesis()
    return response


@router.get("/hash_root", responses={200: {"model": ResponseModelHashRoot}, 503: {"model": ErrorResponseModel}})
@connection_decorator
async def hash_root(
        state_id: str = "head"):
    """
    Calculates HashTreeRoot for state with given 'stateId'. If stateId is root, same value will be returned.
    """
    response = consensus_client.get_hash_root(state_id)
    return response


@router.get("/fork_data", responses={200: {"model": ResponseModelForkData}, 503: {"model": ErrorResponseModel}})
@connection_decorator
async def fork_data(
        state_id: str = "head"):
    """
    Returns Fork object for state with given 'stateId'.
    """
    response = consensus_client.get_fork_data(state_id)
    return response


@router.get("/finality_checkpoint", responses={200: {"model": ResponseModelFinalityCheckpoint}, 503: {"model": ErrorResponseModel}})
@connection_decorator
async def finality_checkpoint(
        state_id: str = "head"):
    """
    Returns finality checkpoints for state with given 'stateId'. In case finality is not yet achieved, checkpoint should return epoch 0 and ZERO_HASH as root.
    """
    response = consensus_client.get_finality_checkpoint(state_id)
    return response


@router.get("/validators", responses={200: {"model": ResponseModelValidators}, 503: {"model": ErrorResponseModel}})
@connection_decorator
async def validators(
        state_id: str = STATE_ID_QUERY_PARAMETER):
    """
    Returns filterable list of validators with their balance, status and index.

    Information will be returned for all indices or public key that match known validators. If an index or public key does not match any known validator, no information will be returned but this will not cause an error. There are no guarantees for the returned data in terms of ordering; both the index and public key are returned for each validator, and can be used to confirm for which inputs a response has been returned.
    """
    # TODO: not working
    response = consensus_client.get_validators(state_id)
    return response


@router.get("/validator", responses={200: {"model": ResponseModelValidator}, 503: {"model": ErrorResponseModel}})
@connection_decorator
async def validator(
        validator_id: int = VALIDATOR_ID_QUERY_PARAMETER,
        state_id: str = STATE_ID_QUERY_PARAMETER):
    """
    Returns validator specified by state and id or public key along with status and balance.
    """
    response = consensus_client.get_validator(validator_id, state_id)
    return response


@router.get("/validator_balances", responses={200: {"model": ResponseModelValidatorBalances}, 503: {"model": ErrorResponseModel}})
@connection_decorator
async def validator_balances(
        state_id: str = STATE_ID_QUERY_PARAMETER):
    """
    Returns filterable list of validators balances.

    Balances will be returned for all indices or public key that match known validators. If an index or public key does not match any known validator, no balance will be returned but this will not cause an error. There are no guarantees for the returned data in terms of ordering; the index and is returned for each balance, and can be used to confirm for which inputs a response has been returned.
    """
    response = consensus_client.get_validator_balances(state_id)
    return response


@router.get("/epoch_committees", responses={200: {"model": ResponseModelEpochCommittees}, 503: {"model": ErrorResponseModel}})
@connection_decorator
async def epoch_committees(
        state_id: str = STATE_ID_QUERY_PARAMETER):
    """
    Retrieves the committees for the given state.
    """
    response = consensus_client.get_epoch_committees(state_id)
    return response


@router.get("/block_headers", responses={200: {"model": ResponseModelBlockHeaders}, 503: {"model": ErrorResponseModel}})
@connection_decorator
async def block_headers():
    """
    Retrieves block headers matching given query. By default it will fetch current head slot blocks.
    """
    response = consensus_client.get_block_headers()
    return response


@router.get("/block_header", responses={200: {"model": ResponseModelBlockHeader}, 503: {"model": ErrorResponseModel}})
@connection_decorator
async def block_header(
        block_id: Union[int, str] = BLOCK_ID_QUERY_PARAMETER):
    """
    Retrieves block header for given block id.
    """
    response = consensus_client.get_block_header(block_id)
    return response


@router.get("/block", responses={200: {"model": ResponseModelBlock}, 503: {"model": ErrorResponseModel}})
@connection_decorator
async def block(
        block_id: Union[int, str] = BLOCK_ID_QUERY_PARAMETER):
    """
    Retrieves block details for given block id. Depending on Accept header it can be returned either as json or as bytes serialized by SSZ
    """
    response = consensus_client.get_block(block_id)
    return response


@router.get("/block_root", responses={200: {"model": ResponseModelBlockRoot}, 503: {"model": ErrorResponseModel}})
@connection_decorator
async def block_root(
        block_id: Union[int, str] = BLOCK_ID_QUERY_PARAMETER):
    """
    Retrieves hashTreeRoot of BeaconBlock/BeaconBlockHeader
    """
    response = consensus_client.get_block_root(block_id)
    return response


@router.get("/block_attestations", responses={200: {"model": ResponseModelBlockAttestations}, 503: {"model": ErrorResponseModel}})
@connection_decorator
async def block_attestations(
        block_id: Union[int, str] = BLOCK_ID_QUERY_PARAMETER):
    """
    Retrieves attestation included in requested block.
    """
    response = consensus_client.get_block_attestations(block_id)
    return response


@router.get("/attestations", responses={200: {"model": ResponseModelAttestations}, 503: {"model": ErrorResponseModel}})
@connection_decorator
async def attestations():
    """
    Retrieves attestations known by the node but not necessarily incorporated into any block
    """
    response = consensus_client.get_attestations()
    return response


@router.get("/attester_slashings", responses={200: {"model": ResponseModelAttesterSlashings}, 503: {"model": ErrorResponseModel}})
@connection_decorator
async def attester_slashings():
    """
    Retrieves attester slashings known by the node but not necessarily incorporated into any block
    """
    # TODO: not working yet (empty response)
    response = consensus_client.get_attester_slashings()
    return response


@router.get("/proposer_slashings", responses={200: {"model": ResponseModelProposerSlashings}, 503: {"model": ErrorResponseModel}})
@connection_decorator
async def proposer_slashings():
    """
    Retrieves proposer slashings known by the node but not necessarily incorporated into any block
    """
    # TODO: not working yet (empty response)
    response = consensus_client.get_proposer_slashings()
    return response


@router.get("/voluntary_exits", responses={200: {"model": ResponseModelVoluntaryExists}, 503: {"model": ErrorResponseModel}})
@connection_decorator
async def voluntary_exits():
    """
    Retrieves voluntary exits known by the node but not necessarily incorporated into any block
    """
    # TODO: not working yet (empty response)
    response = consensus_client.get_voluntary_exits()
    return response
