from dataclasses import dataclass
from typing import List

from soltxs import parser
from soltxs.resolver.models import Resolver, Resolve


@dataclass(slots=True)
class Unknown(Resolve):
    """
    Represents an unknown resolved transaction.
    """


class _UnknownResolver(Resolver):
    """
    Resolver for unknown instructions.
    """

    def resolve(self, instructions: List[parser.models.ParsedInstruction]) -> Resolve:
        """
        Returns an Unknown resolution regardless of input.

        Args:
            instructions: List of parsed instructions.

        Returns:
            An Unknown resolution object.
        """
        return Unknown()


UnknownResolver = _UnknownResolver()
