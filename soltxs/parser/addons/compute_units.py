from dataclasses import dataclass
from typing import Optional

from soltxs.normalizer.models import Transaction
from soltxs.parser.models import Addon, AddonInfo


@dataclass(slots=True)
class ComputeUnits(AddonInfo):
    compute_units_consumed: Optional[int] = None


class _ComputeUnitsAddon(Addon[ComputeUnits]):
    def __init__(self):
        self.addon_name = "compute_units"

    def enrich(self, tx: Transaction) -> Optional[ComputeUnits]:
        if tx.meta.computeUnitsConsumed is not None:
            return ComputeUnits(compute_units_consumed=tx.meta.computeUnitsConsumed)
        return None


ComputeUnitsAddon = _ComputeUnitsAddon()
