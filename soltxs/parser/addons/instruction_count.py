from dataclasses import dataclass
from typing import Dict, List, Optional

from soltxs.normalizer.models import Transaction
from soltxs.parser.models import Addon, AddonInfo, Program


@dataclass(slots=True)
class InstructionCount(AddonInfo):
    counts: Dict[str, int]


class _InstructionCountAddon(Addon[InstructionCount]):
    def __init__(self):
        self.addon_name = "instruction_count"

    def enrich(self, tx: Transaction, parsed_instructions: List[Program]) -> Optional[InstructionCount]:
        counts: Dict[str, int] = {}
        for instr in tx.message.instructions:
            prog_id = tx.message.accountKeys[instr.programIdIndex]
            counts[prog_id] = counts.get(prog_id, 0) + 1
        return InstructionCount(counts=counts) if counts else None


InstructionCountAddon = _InstructionCountAddon()
