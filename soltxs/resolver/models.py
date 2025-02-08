import abc
from dataclasses import dataclass
from typing import List, Optional

from soltxs import parser


@dataclass(slots=True)
class Resolve:
    """
    Base class for a resolved transaction.
    """


class Resolver(abc.ABC):
    """
    Abstract base class for transaction resolvers.
    """

    @abc.abstractmethod
    def resolve(self, instructions: List[parser.models.ParsedInstruction]) -> Optional[Resolve]:
        """
        Resolves parsed instructions into a human-readable transaction.

        Args:
            instructions: List of parsed instructions.

        Returns:
            A resolved transaction object or None if not resolvable.
        """
        raise NotImplementedError
