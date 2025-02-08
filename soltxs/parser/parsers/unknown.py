from dataclasses import dataclass
from typing import Union

from soltxs.normalizer.models import Transaction
from soltxs.parser.models import ParsedInstruction, Program


@dataclass(slots=True)
class Unknown(ParsedInstruction):
    instruction_index: int


ParsedInstructions = Union[Unknown]


class UnknownParser(Program):
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
        return Unknown(
            program_id=self.program_id,
            program_name=self.program_name,
            instruction_name="Unknown",
            instruction_index=instruction_index,
        )
