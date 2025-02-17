from dataclasses import dataclass
from typing import List, Optional

from soltxs import parser
from soltxs.parser.parsers.pumpfun import WSOL_MINT, Swap
from soltxs.resolver.models import Resolve, Resolver

LAMPORTS_PER_SOL = 1e9


@dataclass(slots=True)
class PumpFun(Resolve):
    """
    Represents a resolved PumpFun transaction.

    Attributes:
        type: The instruction type ('buy' or 'sell').
        who: The user performing the transaction.
        from_token: The token being exchanged from.
        from_amount: Amount exchanged from (in SOL for SOL amounts).
        to_token: The token being exchanged to.
        to_amount: Amount exchanged to (in SOL for SOL amounts).
    """

    type: str
    who: str
    from_token: str
    from_amount: float
    to_token: str
    to_amount: float


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
            A PumpFun resolved object if exactly one Swap instruction is found, else None.
        """
        instrs = [i for i in instructions if isinstance(i, Swap)]
        if len(instrs) == 1:
            instr = instrs[0]
            if instr.is_buy:
                p_type = "buy"
                from_token = WSOL_MINT
                to_token = instr.mint
                resolved_from_amount = instr.sol_amount / LAMPORTS_PER_SOL
                resolved_to_amount = instr.token_amount
            else:
                p_type = "sell"
                from_token = instr.mint
                to_token = WSOL_MINT
                resolved_from_amount = instr.token_amount
                resolved_to_amount = instr.sol_amount / LAMPORTS_PER_SOL

            return PumpFun(
                type=p_type,
                who=instr.user,
                from_token=from_token,
                from_amount=resolved_from_amount,
                to_token=to_token,
                to_amount=resolved_to_amount,
            )
        return None


PumpFunResolver = _PumpFunResolver()
