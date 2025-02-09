from typing import List

from soltxs.normalizer import models
from soltxs.normalizer.normalizers import shared


def normalize(tx: dict) -> models.Transaction:
    """
    Parses an RPC transaction response into a standardized Transaction.

    Args:
        tx: An RPC transaction response.

    Returns:
        A standardized Transaction object.
    """
    result = tx["result"]

    slot = result["slot"]
    block_time = result.get("blockTime")
    transaction_dict = result["transaction"]
    meta = result["meta"]

    # Consolidate loadedAddresses from meta.
    loaded_addresses = models.LoadedAddresses(
        writable=meta.get("loadedAddresses", {}).get("writable", []),
        readonly=meta.get("loadedAddresses", {}).get("readonly", []),
    )

    # Parse instructions using shared helper.
    raw_instructions = transaction_dict["message"]["instructions"]
    instructions: List[models.Instruction] = [shared.instructions(i) for i in raw_instructions]

    # Parse address table lookups if present.
    raw_lookups = transaction_dict["message"].get("addressTableLookups", [])
    address_table_lookups: List[models.AddressTableLookup] = [shared.address_lookup(lu) for lu in raw_lookups]

    # Normalize program IDs in accountKeys.
    account_keys = shared.program_id(transaction_dict["message"]["accountKeys"])

    # Parse token balances.
    raw_pre_tb = meta.get("preTokenBalances", [])
    raw_post_tb = meta.get("postTokenBalances", [])
    pre_token_balances = [shared.token_balance(tb) for tb in raw_pre_tb]
    post_token_balances = [shared.token_balance(tb) for tb in raw_post_tb]

    return models.Transaction(
        slot=slot,
        blockTime=block_time,
        signatures=transaction_dict["signatures"],
        message=models.Message(
            accountKeys=account_keys,
            recentBlockhash=transaction_dict["message"]["recentBlockhash"],
            instructions=instructions,
            addressTableLookups=address_table_lookups,
        ),
        meta=models.Meta(
            fee=meta.get("fee", 0),
            preBalances=meta.get("preBalances", []),
            postBalances=meta.get("postBalances", []),
            preTokenBalances=pre_token_balances,
            postTokenBalances=post_token_balances,
            innerInstructions=meta.get("innerInstructions", []),
            logMessages=meta.get("logMessages", []),
            err=meta.get("err"),
            status=meta.get("status", {}),
            computeUnitsConsumed=meta.get("computeUnitsConsumed"),
        ),
        loadedAddresses=loaded_addresses,
    )
