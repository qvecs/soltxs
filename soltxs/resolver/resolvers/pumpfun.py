from dataclasses import dataclass
from typing import List, Optional

from soltxs import parser
from soltxs.resolver.models import Resolve, Resolver


@dataclass(slots=True)
class PumpFun(Resolve):
    """
    Represents a resolved PumpFun transaction.

    Attributes:
        type: The instruction type ('Buy' or 'Sell').
        who: The user performing the transaction.
        from_token: The token being sold.
        from_amount: Amount sold (adjusted for decimals).
        to_token: The token being bought.
        to_amount: Amount bought (adjusted for decimals).
    """

    type: str
    who: str
    from_token: str
    from_amount: int
    to_token: str
    to_amount: int


class _PumpFunResolver(Resolver):
    """
    Resolver for PumpFun instructions.
    """

    def resolve(self, instructions: List[parser.models.ParsedInstruction]) -> Optional[Resolve]:
        """
        Resolves PumpFun instructions.

        Args:
            instructions: List of parsed instructions.

        Returns:
            A PumpFun resolved object if exactly one Buy/Sell instruction is found, else None.
        """
        instrs = [i for i in instructions if isinstance(i, (parser.parsers.pumpfun.Buy, parser.parsers.pumpfun.Sell))]
        if len(instrs) == 1:
            instr = instrs[0]
            return PumpFun(
                type=instr.instruction_name.lower(),
                who=instr.who,
                from_token=instr.from_token,
                from_amount=instr.from_token_amount / 10**instr.from_token_decimals,
                to_token=instr.to_token,
                to_amount=instr.to_token_amount / 10**instr.to_token_decimals,
            )


PumpFunResolver = _PumpFunResolver()
