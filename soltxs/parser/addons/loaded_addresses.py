from typing import Any, Dict, Optional

from soltxs.normalizer.models import Transaction
from soltxs.parser.models import Addon


class _LoadedAddressesAddon(Addon):
    def __init__(self):
        self.addon_name = "loaded_addresses"

    def enrich(self, tx: Transaction) -> Optional[Dict[str, Any]]:
        writable = tx.loadedAddresses.writable
        readonly = tx.loadedAddresses.readonly
        if writable or readonly:
            return {"writable": writable, "readonly": readonly}
        return None


LoadedAddressesAddon = _LoadedAddressesAddon()
