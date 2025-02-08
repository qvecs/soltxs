from typing import Any, Dict, Optional

from soltxs.normalizer.models import Transaction
from soltxs.parser.models import Addon

PLATFORM = {
    "tro46jTMkb56A3wPepo5HT7JcvX9wFWvR8VaJzgdjEf": "Trojan",
    "9RYJ3qr5eU5xAooqVcbmdeusjcViL5Nkiq7Gske3tiKq": "BullX",
    "AVUCZyuT35YSuj4RH7fwiyPu82Djn2Hfg7y2ND2XcnZH": "Photon",
}


class _PlatformIdentifierAddon(Addon):
    def __init__(self):
        self.addon_name = "platform_identifier"

    def enrich(self, tx: Transaction) -> Optional[Dict[str, Any]]:
        for address in tx.all_accounts:
            if address in PLATFORM:
                return {"address": address, "name": PLATFORM[address]}
        return None


PlatformIdentifierAddon = _PlatformIdentifierAddon()
