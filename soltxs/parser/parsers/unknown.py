from dataclasses import dataclass
from typing import Union

from soltxs.normalizer.models import Transaction
from soltxs.parser.models import ParsedInstruction, Program


@dataclass(slots=True)
class Unknown(ParsedInstruction):
    """
    Parsed instruction representing an unknown instruction.

    Attributes:
        instruction_index: The index of the unknown instruction.
    """

    instruction_index: int


ParsedInstructions = Union[Unknown]


class UnknownParser(Program):
    """
    Parser for unknown instructions.
    """

    def __init__(self, program_id: str):
        self.program_id = program_id
        self.program_name = "Unknown"
        self.desc = lambda d: True
        self.desc_map = {True: self.process_Unknown}

    def process_Unknown(
        self,
        tx: Transaction,
        instruction_index: int,
        decoded_data: bytes,
    ) -> ParsedInstructions:
        """
        Processes an unknown instruction.

        Args:
            tx: The Transaction object.
            instruction_index: Index of the instruction.
            decoded_data: Decoded instruction data.

        Returns:
            An Unknown parsed instruction.
        """
        return Unknown(
            program_id=self.program_id,
            program_name=self.program_name,
            instruction_name="Unknown",
            instruction_index=instruction_index,
        )
