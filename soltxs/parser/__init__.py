from typing import Any, Dict, List

from soltxs.normalizer.models import Transaction
from soltxs.parser import addons, models, parsers

# Map program IDs to their corresponding parser classes.
id_to_handler: Dict[str, models.Program] = {
    parsers.systemProgram.SystemProgramParser.program_id: parsers.systemProgram.SystemProgramParser,
    parsers.computeBudget.ComputeBudgetParser.program_id: parsers.computeBudget.ComputeBudgetParser,
    parsers.tokenProgram.TokenProgramParser.program_id: parsers.tokenProgram.TokenProgramParser,
    parsers.raydiumAMM.RaydiumAMMParser.program_id: parsers.raydiumAMM.RaydiumAMMParser,
    parsers.pumpfun.PumpFunParser.program_id: parsers.pumpfun.PumpFunParser,
}

# List of addon enrichers for additional data.
addon_enrichers: List[models.Addon] = [
    addons.compute_units.ComputeUnitsAddon,
    addons.instruction_count.InstructionCountAddon,
    addons.loaded_addresses.LoadedAddressesAddon,
    addons.platform_identifier.PlatformIdentifierAddon,
    addons.token_transfer.TokenTransferSummaryAddon,
]


def parse(tx: Transaction) -> Dict[str, Any]:
    """
    Parses a normalized transaction into its component instructions and addon data.

    Args:
        tx: A normalized Transaction object.

    Returns:
        A dictionary containing:
          - "signatures": List of transaction signatures.
          - "instructions": List of parsed instruction objects.
          - "addons": Dictionary of addon enrichment data.
    """
    parsed_instructions = []

    for idx, instruction in enumerate(tx.message.instructions):
        # Determine the program id for the instruction.
        program_id = tx.message.accountKeys[instruction.programIdIndex]
        # Select the appropriate parser; default to UnknownParser if not found.
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
