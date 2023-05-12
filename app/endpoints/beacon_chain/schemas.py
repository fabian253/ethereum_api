from pydantic import BaseModel, Field
from typing import Any, List, Dict, Union, Optional


class ResponseModelGenesis(BaseModel):
    class Data(BaseModel):
        genesis_time: str
        genesis_validators_root: str
        genesis_fork_version: str

    data: Data


class ResponseModelHashRoot(BaseModel):
    class Data(BaseModel):
        root: str

    data: Data
    execution_optimistic: bool
    finalized: bool


class ResponseModelForkData(BaseModel):
    class Data(BaseModel):
        previous_version: str
        current_version: str
        epoch: str

    data: Data
    execution_optimistic: bool
    finalized: bool


class ResponseModelFinalityCheckpoint(BaseModel):
    class Data(BaseModel):
        class PreviousJustified(BaseModel):
            epoch: str
            root: str

        class CurrentJustified(BaseModel):
            epoch: str
            root: str

        class Finalized(BaseModel):
            epoch: str
            root: str

        previous_justified: PreviousJustified
        current_justified: CurrentJustified
        finalized: Finalized

    data: Data
    execution_optimistic: bool
    finalized: bool


class ResponseModelValidators(BaseModel):
    # TODO: Endpoint not working
    class Data(BaseModel):
        class Validator(BaseModel):
            pubkey: str
            withdrawal_credentials: str
            effective_balance: str
            slashed: bool
            activation_eligibility_epoch: str
            activation_epoch: str
            exit_epoch: str
            withdrawable_epoch: str

        index: str
        balance: str
        status: str
        validator: Validator

    execution_optimistic: bool
    data: List[Data]


class ResponseModelValidator(BaseModel):
    class Data(BaseModel):
        class Validator(BaseModel):
            pubkey: str
            withdrawal_credentials: str
            effective_balance: str
            slashed: bool
            activation_eligibility_epoch: str
            activation_epoch: str
            exit_epoch: str
            withdrawable_epoch: str

        index: str
        balance: str
        status: str
        validator: Validator

    execution_optimistic: bool
    data: Data


class ResponseModelValidatorBalances(BaseModel):
    class Data(BaseModel):
        index: str
        balance: str

    execution_optimistic: bool
    data: List[Data]


class ResponseModelEpochCommittees(BaseModel):
    class Data(BaseModel):
        index: str
        slot: str
        validators: List[str]

    data: List[Data]
    execution_optimistic: bool
    finalized: bool


class ResponseModelBlockHeaders(BaseModel):
    class Data(BaseModel):
        class Header(BaseModel):
            class Message(BaseModel):
                slot: str
                proposer_index: str
                parent_root: str
                state_root: str
                body_root: str

            message: Message
            signature: str

        root: str
        canonical: bool
        header: Header

    data: List[Data]
    execution_optimistic: bool
    finalized: bool


class ResponseModelBlockHeader(BaseModel):
    class Data(BaseModel):
        class Header(BaseModel):
            class Message(BaseModel):
                slot: str
                proposer_index: str
                parent_root: str
                state_root: str
                body_root: str

            message: Message
            signature: str

        root: str
        canonical: bool
        header: Header

    data: Data
    execution_optimistic: bool
    finalized: bool


class ResponseModelBlock(BaseModel):
    class Data(BaseModel):
        class Message(BaseModel):
            class Body(BaseModel):
                class Eth1Data(BaseModel):
                    deposit_root: str
                    deposit_count: str
                    block_hash: str

                class Attestation(BaseModel):
                    class Data1(BaseModel):
                        class Source(BaseModel):
                            epoch: str
                            root: str

                        class Target(BaseModel):
                            epoch: str
                            root: str

                        slot: str
                        index: str
                        beacon_block_root: str
                        source: Source
                        target: Target

                    aggregation_bits: str
                    data: Data1
                    signature: str

                randao_reveal: str
                eth1_data: Eth1Data
                graffiti: str
                proposer_slashings: List
                attester_slashings: List
                attestations: List[Attestation]
                deposits: List
                voluntary_exits: List

            slot: str
            proposer_index: str
            parent_root: str
            state_root: str
            body: Body

        message: Message
        signature: str

    data: Data


class ResponseModelBlockRoot(BaseModel):
    class Data(BaseModel):
        root: str

    data: Data
    execution_optimistic: bool
    finalized: bool


class ResponseModelBlockAttestations(BaseModel):
    class Data(BaseModel):

        class Data(BaseModel):
            class Source(BaseModel):
                epoch: str
                root: str

            class Target(BaseModel):
                epoch: str
                root: str

            slot: str
            index: str
            beacon_block_root: str
            source: Source
            target: Target

        aggregation_bits: str
        data: Data
        signature: str

    data: List[Data]
    execution_optimistic: bool
    finalized: bool


class ResponseModelAttestations(BaseModel):
    class Data(BaseModel):
        class Data(BaseModel):
            class Source(BaseModel):
                epoch: str
                root: str

            class Target(BaseModel):
                epoch: str
                root: str

            slot: str
            index: str
            beacon_block_root: str
            source: Source
            target: Target

        aggregation_bits: str
        data: Data
        signature: str

    data: List[Data]


class ResponseModelAttesterSlashings(BaseModel):
    # TODO: method and endpoint not working
    class Data(BaseModel):
        pass

    data: List


class ResponseModelProposerSlashings(BaseModel):
    # TODO: method and endpoint not working
    class Data(BaseModel):
        pass

    data: List


class ResponseModelVoluntaryExists(BaseModel):
    # TODO: method and endpoint not working
    class Data(BaseModel):
        pass

    data: List


class ErrorResponseModel(BaseModel):
    status_code: int
    detail: str
