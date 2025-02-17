from dataclasses import dataclass
from typing import List, Optional

from soltxs import parser
from soltxs.resolver.models import Resolve, Resolver

WSOL_MINT = "So11111111111111111111111111111111111111112"
SOL_MINT = "11111111111111111111111111111111"
LAMPORTS_PER_SOL = 1e9


@dataclass(slots=True)
class Raydium(Resolve):
    """
    Represents a resolved Raydium transaction.

    Attributes:
        type: The type of swap (e.g., 'swap', 'buy', 'sell').
        who: The user account performing the swap.
        from_token: The token being sold.
        from_amount: Amount sold.
        to_token: The token being bought.
        to_amount: Amount bought.
        minimum_amount_out: The minimum amount expected.
    """

    type: str
    who: str
    from_token: str
    from_amount: float
    to_token: str
    to_amount: float
    minimum_amount_out: float


class _RaydiumResolver(Resolver):
    """
    Resolver for Raydium AMM instructions.
    """

    def resolve(self, instructions: List[parser.models.ParsedInstruction]) -> Optional[Resolve]:
        """
        Resolves Raydium swap instructions from parsed instructions.

        Args:
            instructions: List of parsed instructions.

        Returns:
            A Raydium resolved object if a swap instruction is found, else None.
        """
        instrs = [i for i in instructions if isinstance(i, parser.parsers.raydiumAMM.Swap)]
        if len(instrs) == 1:
            instr = instrs[0]

            raydium_type = "swap"
            if instr.from_token in {WSOL_MINT, SOL_MINT}:
                raydium_type = "buy"
            elif instr.to_token in {WSOL_MINT, SOL_MINT}:
                raydium_type = "sell"

            if instr.from_token in {WSOL_MINT, SOL_MINT}:
                resolved_from_amount = instr.from_token_amount / LAMPORTS_PER_SOL
            else:
                resolved_from_amount = instr.from_token_amount / 10**instr.from_token_decimals

            if instr.to_token in {WSOL_MINT, SOL_MINT}:
                resolved_to_amount = instr.to_token_amount / LAMPORTS_PER_SOL
                resolved_minimum_amount_out = instr.minimum_amount_out / LAMPORTS_PER_SOL
            else:
                resolved_to_amount = instr.to_token_amount / 10**instr.to_token_decimals
                resolved_minimum_amount_out = instr.minimum_amount_out / 10**instr.to_token_decimals

            return Raydium(
                type=raydium_type,
                who=instr.who,
                from_token=instr.from_token,
                from_amount=resolved_from_amount,
                to_token=instr.to_token,
                to_amount=resolved_to_amount,
                minimum_amount_out=resolved_minimum_amount_out,
            )
        return None


RaydiumResolver = _RaydiumResolver()
