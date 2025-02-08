from typing import Any, Dict, Optional

from soltxs.normalizer.models import Transaction
from soltxs.parser.models import Addon


class _ComputeUnitsAddon(Addon):
    def __init__(self):
        self.addon_name = "compute_units"

    def enrich(self, tx: Transaction) -> Optional[Dict[str, Any]]:
        if tx.meta.computeUnitsConsumed is not None:
            return {"compute_units_consumed": tx.meta.computeUnitsConsumed}
        return None


ComputeUnitsAddon = _ComputeUnitsAddon()
