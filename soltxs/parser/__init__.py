from dataclasses import make_dataclass
from typing import Dict, List, Optional

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
    addons.transaction_status.TransactionStatusAddon,
]

# Dynamic dataclass for addon enrichment data.
Addons = make_dataclass("Addons", [(addon.addon_name, addon.enrich.__annotations__.get("return", object), None) for addon in addon_enrichers])


def parse(tx: Transaction) -> models.ParsedTransaction:
    """
    Parses a normalized transaction into its component instructions and addon data.

    Args:
        tx: A normalized Transaction object.

    Returns:
        A ParsedTransaction object with the parsed instructions and addon data.
    """
    parsed_instructions = []

    for idx, instruction in enumerate(tx.message.instructions):
        program_id = tx.message.accountKeys[instruction.programIdIndex]

        router = id_to_handler.get(program_id, parsers.unknown.UnknownParser(program_id))
        action = router.route(tx, idx)

        parsed_instructions.append(action)

    addons = Addons()
    for addon in addon_enrichers:
        result = addon.enrich(tx, parsed_instructions)
        if result is not None:
            setattr(addons, addon.addon_name, result)

    return models.ParsedTransaction(
        signatures=tx.signatures,
        instructions=parsed_instructions,
        addons=addons,
    )
