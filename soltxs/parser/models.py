import abc
from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Generic, Optional, TypeVar

import qbase58 as base58

from soltxs.normalizer.models import Instruction, Transaction


@dataclass
class ParsedInstruction:
    """
    Base class for a parsed instruction.

    Attributes:
        program_id: The program ID that processed the instruction.
        program_name: The name of the program.
        instruction_name: The specific instruction name.
    """

    program_id: str
    program_name: str
    instruction_name: str


T = TypeVar("T", bound=ParsedInstruction)


class Program(abc.ABC, Generic[T]):
    """
    Abstract base class for program parsers.

    Attributes:
        program_id: The unique program identifier.
        program_name: The name of the program.
        desc: A callable that extracts the discriminator from instruction data.
        desc_map: A mapping from discriminator values to parser functions.
    """

    program_id: str
    program_name: str

    # Discriminator extraction function.
    desc: callable
    desc_map: Dict[bytes | int, callable]

    def route(self, tx: Transaction, instruction_index: int) -> T:
        """
        Route the instruction to the correct parser based on the discriminator.

        Notes:
            The discriminator is extracted from the instruction data using the 'desc'
            function. This value is then used to select the appropriate parser from
            'desc_map'. If no parser is found for the discriminator, a NotImplementedError
            is raised.

        Args:
            tx: The Transaction object.
            instruction_index: The index of the instruction within the transaction.

        Returns:
            A parsed instruction object.

        Raises:
            NotImplementedError: If the discriminator is unknown.
        """
        instr: Instruction = tx.message.instructions[instruction_index]

        decoded_data = base58.decode(instr.data or "")
        discriminator = self.desc(decoded_data)
        parser_func = self.desc_map.get(discriminator, self.desc_map.get("default"))
        if not parser_func:
            raise NotImplementedError(f"Unknown {self.__class__.__name__} discriminator: {discriminator}")

        return parser_func(tx, instruction_index, decoded_data)

class Addon(abc.ABC):
    """
    Abstract base class for addon enrichers.
    """

    addon_name: str

    @abstractmethod
    def enrich(self, tx: Transaction) -> Optional[Dict[str, Any]]:
        """
        Enriches the given transaction and returns a dictionary of extra data.
        If no enrichment is available, return None.

        Args:
            tx: The normalized Transaction object.

        Returns:
            A dictionary with enrichment data or None.
        """
