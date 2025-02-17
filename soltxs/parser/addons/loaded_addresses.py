from dataclasses import dataclass
from typing import List, Optional

from soltxs.normalizer.models import Transaction
from soltxs.parser.models import Addon, AddonInfo, Program


@dataclass(slots=True)
class LoadedAddresses(AddonInfo):
    writable: List[str]
    readonly: List[str]


class _LoadedAddressesAddon(Addon[LoadedAddresses]):
    def __init__(self):
        self.addon_name = "loaded_addresses"

    def enrich(self, tx: Transaction, parsed_instructions: List[Program]) -> Optional[LoadedAddresses]:
        writable = tx.loadedAddresses.writable
        readonly = tx.loadedAddresses.readonly
        if writable or readonly:
            return LoadedAddresses(writable=writable, readonly=readonly)
        return None


LoadedAddressesAddon = _LoadedAddressesAddon()
