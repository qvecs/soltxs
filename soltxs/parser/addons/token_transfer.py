from dataclasses import dataclass
from typing import Dict, List, Optional

from soltxs.normalizer.models import Transaction
from soltxs.parser.models import Addon, AddonInfo, Program


@dataclass(slots=True)
class TokenTransfer(AddonInfo):
    net_changes: Dict[str, int]


class _TokenTransferSummaryAddon(Addon[TokenTransfer]):
    def __init__(self):
        self.addon_name = "token_transfer_summary"

    def enrich(self, tx: Transaction, parsed_instructions: List[Program]) -> Optional[TokenTransfer]:
        pre_totals: Dict[str, int] = {}
        for tb in tx.meta.preTokenBalances:
            mint = tb.mint
            amount = int(tb.uiTokenAmount.amount)
            pre_totals[mint] = pre_totals.get(mint, 0) + amount

        post_totals: Dict[str, int] = {}
        for tb in tx.meta.postTokenBalances:
            mint = tb.mint
            amount = int(tb.uiTokenAmount.amount)
            post_totals[mint] = post_totals.get(mint, 0) + amount

        net_changes: Dict[str, int] = {}
        for mint in set(list(pre_totals.keys()) + list(post_totals.keys())):
            net_changes[mint] = post_totals.get(mint, 0) - pre_totals.get(mint, 0)
        return TokenTransfer(net_changes=net_changes) if net_changes else None


TokenTransferSummaryAddon = _TokenTransferSummaryAddon()
