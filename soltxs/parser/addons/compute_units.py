from dataclasses import dataclass
from typing import List, Optional

from soltxs.normalizer.models import Transaction
from soltxs.parser.models import Addon, AddonInfo, Program
from soltxs.parser.parsers.computeBudget import SetComputeUnitLimit, SetComputeUnitPrice

MICRO_LAMPORTS_PER_SOL = 1e15


@dataclass(slots=True)
class ComputeUnits(AddonInfo):
    compute_units_consumed: Optional[int] = None
    compute_unit_limit: Optional[int] = None
    compute_unit_price_micro_lamports: Optional[int] = None
    compute_cost_sol: Optional[int] = None
    remaining_compute_units: Optional[int] = None


class _ComputeUnitsAddon(Addon[ComputeUnits]):
    def __init__(self):
        self.addon_name = "compute_units"

    def enrich(self, tx: Transaction, parsed_instructions: List[Program]) -> Optional[ComputeUnits]:
        consumed = tx.meta.computeUnitsConsumed
        limit, price = None, None
        for instr in parsed_instructions:
            if isinstance(instr, SetComputeUnitLimit):
                limit = instr.compute_unit_limit
            elif isinstance(instr, SetComputeUnitPrice):
                price = instr.micro_lamports

        if consumed is None and limit is None and price is None:
            return None

        compute_cost = consumed * price if (consumed is not None and price is not None) else None
        compute_cost_sol = (compute_cost / MICRO_LAMPORTS_PER_SOL) if compute_cost is not None else None
        remaining_compute_units = (limit - consumed) if (limit is not None and consumed is not None) else None

        return ComputeUnits(
            compute_units_consumed=consumed,
            compute_unit_limit=limit,
            compute_unit_price_micro_lamports=price,
            compute_cost_sol=compute_cost_sol,
            remaining_compute_units=remaining_compute_units,
        )


ComputeUnitsAddon = _ComputeUnitsAddon()
