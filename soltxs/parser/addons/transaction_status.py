from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List, Optional

from soltxs.normalizer.models import Transaction
from soltxs.parser.models import Addon, AddonInfo, Program


@dataclass(slots=True)
class TransactionStatus(AddonInfo):
    """
    Provides the timestamp, slot, and age (in minutes) for the transaction.

    Attributes:
        timestamp: ISO formatted timestamp string or None if unavailable.
        slot: The slot number of the transaction.
    """

    timestamp: Optional[str]
    slot: int


class _TransactionStatusAddon(Addon[TransactionStatus]):
    def __init__(self):
        self.addon_name = "transaction_status"

    def enrich(self, tx: Transaction, parsed_instructions: List[Program]) -> Optional[TransactionStatus]:
        if tx.blockTime is not None:
            ts = datetime.fromtimestamp(tx.blockTime, tz=timezone.utc)
            timestamp = ts.isoformat()
        else:
            timestamp = None

        return TransactionStatus(timestamp=timestamp, slot=tx.slot)


TransactionStatusAddon = _TransactionStatusAddon()
