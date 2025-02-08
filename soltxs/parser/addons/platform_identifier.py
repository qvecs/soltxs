from typing import Optional, Tuple

from soltxs.normalizer.models import Transaction

PLATFORM = {
    "tro46jTMkb56A3wPepo5HT7JcvX9wFWvR8VaJzgdjEf": "Trojan",
    "9RYJ3qr5eU5xAooqVcbmdeusjcViL5Nkiq7Gske3tiKq": "BullX",
    "AVUCZyuT35YSuj4RH7fwiyPu82Djn2Hfg7y2ND2XcnZH": "Photon",
}


def enrich(tx: Transaction) -> Tuple[Optional[str], Optional[str]]:
    """
    Identifies the platform of the transaction based on known addresses.

    Args:
        tx: The Transaction object.

    Returns:
        A tuple containing the platform address and platform name if found, otherwise (None, None).
    """
    for address in tx.all_accounts:
        if address in PLATFORM:
            return address, PLATFORM[address]

    return None, None
