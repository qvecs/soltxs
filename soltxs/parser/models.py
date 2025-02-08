import abc
from dataclasses import dataclass
from typing import Dict, Generic, TypeVar

import qbase58 as base58

from soltxs.normalizer.models import Instruction, Transaction


@dataclass
class ParsedInstruction:
    program_id: str
    program_name: str
    instruction_name: str


T = TypeVar("T", bound=ParsedInstruction)


class Program(abc.ABC, Generic[T]):
    program_id: str
    program_name: str

    # Descriminator information.
    desc: callable
    desc_map: Dict[bytes | int, callable]

    def route(self, tx: Transaction, instruction_index: int) -> T:
        """
        Route the instruction to the correct parser based on the descriminator.

        Notes:
            Descriminators can be any byte or integer value in the instruction
            data. That is defined by 'desc', which is a lambda function that
            extracts the descriminator from the instruction data. The
            descriminator is then used to route the instruction to the correct
            parser via 'desc_map', which is a dictionary of descriminators and
            their corresponding parser functions.

        Args:
            tx: The transaction object.
            instruction_index: The index of the instruction in the transaction.

        Returns:
            The parsed instruction object
        """
        instr: Instruction = tx.message.instructions[instruction_index]

        decoded_data = base58.decode(instr.data)
        descriminator = self.desc(decoded_data)
        parser = self.desc_map.get(descriminator, self.desc_map.get("default"))
        if not parser:
            raise NotImplementedError(f"Unknown {self.__class__.__name__} descriminator: {descriminator}")

        return parser(tx, instruction_index, decoded_data)
