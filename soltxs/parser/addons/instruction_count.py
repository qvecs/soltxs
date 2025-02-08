from typing import Any, Dict, Optional
from soltxs.normalizer.models import Transaction
from soltxs.parser.models import Addon


class _InstructionCountAddon(Addon):
    def __init__(self):
        self.addon_name = "instruction_count"

    def enrich(self, tx: Transaction) -> Optional[Dict[str, Any]]:
        counts: Dict[str, int] = {}
        for instr in tx.message.instructions:
            prog_id = tx.message.accountKeys[instr.programIdIndex]
            counts[prog_id] = counts.get(prog_id, 0) + 1
        return counts if counts else None


InstructionCountAddon = _InstructionCountAddon()
