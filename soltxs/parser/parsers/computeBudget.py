from __future__ import annotations

from dataclasses import dataclass
from typing import Union

from soltxs.normalizer.models import Transaction
from soltxs.parser.models import ParsedInstruction, Program


@dataclass(slots=True)
class SetComputeUnitLimit(ParsedInstruction):
    """
    Parsed instruction for setting compute unit limit.

    Attributes:
        compute_unit_limit: The new compute unit limit.
    """

    compute_unit_limit: int


@dataclass(slots=True)
class SetComputeUnitPrice(ParsedInstruction):
    """
    Parsed instruction for setting compute unit price.

    Attributes:
        micro_lamports: The price per compute unit in micro lamports.
    """

    micro_lamports: int


ParsedInstructions = Union[SetComputeUnitLimit, SetComputeUnitPrice]


class _ComputeBudgetParser(Program[ParsedInstructions]):
    """
    Parser for the Compute Budget program.
    """

    def __init__(self):
        self.program_id = "ComputeBudget111111111111111111111111111111"
        self.program_name = "ComputeBudget"
        self.desc = lambda d: d[0]
        self.desc_map = {
            2: self.process_SetComputeUnitLimit,
            3: self.process_SetComputeUnitPrice,
        }

    def process_SetComputeUnitLimit(
        self,
        tx: Transaction,
        instruction_index: int,
        decoded_data: bytes,
    ) -> SetComputeUnitLimit:
        """
        Processes a SetComputeUnitLimit instruction.

        Args:
            tx: The Transaction object.
            instruction_index: Index of the instruction.
            decoded_data: Decoded instruction data.

        Returns:
            A SetComputeUnitLimit parsed instruction.
        """
        return SetComputeUnitLimit(
            program_id=self.program_id,
            program_name=self.program_name,
            instruction_name="SetComputeUnitLimit",
            compute_unit_limit=int.from_bytes(decoded_data[1:5], byteorder="little", signed=False),
        )

    def process_SetComputeUnitPrice(
        self,
        tx: Transaction,
        instruction_index: int,
        decoded_data: bytes,
    ) -> SetComputeUnitPrice:
        """
        Processes a SetComputeUnitPrice instruction.

        Args:
            tx: The Transaction object.
            instruction_index: Index of the instruction.
            decoded_data: Decoded instruction data.

        Returns:
            A SetComputeUnitPrice parsed instruction.
        """
        return SetComputeUnitPrice(
            program_id=self.program_id,
            program_name=self.program_name,
            instruction_name="SetComputeUnitPrice",
            micro_lamports=int.from_bytes(decoded_data[1:9], byteorder="little", signed=False),
        )


ComputeBudgetParser = _ComputeBudgetParser()
