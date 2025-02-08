from typing import Any, Dict, List

from soltxs.normalizer.models import Transaction
from soltxs.parser import addons, models, parsers

id_to_handler: Dict[str, models.Program] = {
    parsers.systemProgram.SystemProgramParser.program_id: parsers.systemProgram.SystemProgramParser,
    parsers.computeBudget.ComputeBudgetParser.program_id: parsers.computeBudget.ComputeBudgetParser,
    parsers.tokenProgram.TokenProgramParser.program_id: parsers.tokenProgram.TokenProgramParser,
    parsers.raydiumAMM.RaydiumAMMParser.program_id: parsers.raydiumAMM.RaydiumAMMParser,
    parsers.pumpfun.PumpFunParser.program_id: parsers.pumpfun.PumpFunParser,
}

addon_enrichers: List[models.Addon] = [
    addons.compute_units.ComputeUnitsAddon,
    addons.instruction_count.InstructionCountAddon,
    addons.loaded_addresses.LoadedAddressesAddon,
    addons.platform_identifier.PlatformIdentifierAddon,
    addons.token_transfer.TokenTransferSummaryAddon,
]


def parse(tx: Transaction) -> Dict[str, Any]:
    parsed_instructions = []

    for idx, instruction in enumerate(tx.message.instructions):
        program_id = tx.message.accountKeys[instruction.programIdIndex]
        router = id_to_handler.get(program_id, parsers.unknown.UnknownParser(program_id))
        action = router.route(tx, idx)
        parsed_instructions.append(action)

    addons_result: Dict[str, Any] = {}
    for addon in addon_enrichers:
        result = addon.enrich(tx)
        if result is not None:
            addons_result[addon.addon_name] = result

    return {
        "signatures": tx.signatures,
        "instructions": parsed_instructions,
        "addons": addons_result,
    }
