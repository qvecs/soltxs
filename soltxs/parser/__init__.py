from typing import Dict, List

from soltxs.normalizer.models import Transaction
from soltxs.parser import models, parsers

id_to_handler: Dict[str, models.Program] = {
    parsers.systemProgram.SystemProgramParser.program_id: parsers.systemProgram.SystemProgramParser,
    parsers.computeBudget.ComputeBudgetParser.program_id: parsers.computeBudget.ComputeBudgetParser,
    parsers.tokenProgram.TokenProgramParser.program_id: parsers.tokenProgram.TokenProgramParser,
    parsers.raydiumAMM.RaydiumAMMParser.program_id: parsers.raydiumAMM.RaydiumAMMParser,
    parsers.pumpfun.PumpFunParser.program_id: parsers.pumpfun.PumpFunParser,
}


def parse(tx: Transaction) -> List[models.ParsedInstruction]:
    """
    Parses a standardized Solana transaction object.
    """

    actions: List[models.ParsedInstruction] = []

    for idx, instruction in enumerate(tx.message.instructions):
        program_id = tx.message.accountKeys[instruction.programIdIndex]

        router = id_to_handler.get(program_id, parsers.unknown.UnknownParser(program_id))
        action = router.route(tx, idx)
        actions.append(action)

    return actions
