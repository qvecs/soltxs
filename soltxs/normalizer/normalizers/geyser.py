from typing import List

from soltxs.normalizer import models
from soltxs.normalizer.normalizers import shared


def normalize(tx: dict) -> models.Transaction:
    """
    Standardizes a Geyser-style transaction response.

    Notes:
        This Geyser-style transaction uses a modified version of the
        YellowStone Geyser Protobuf format. For standard Geyser Protobuf,
        as defined in the YellowStone-gRPC repo, a new normalizer will
        be required.

    Args:
        tx: A Geyser-style transaction response.

    Returns:
        A standardized Transaction object.
    """
    txn_container = tx["transaction"]
    slot = txn_container["slot"]
    geyser_txn = txn_container["transaction"]
    geyser_meta = geyser_txn["meta"]

    real_txn = geyser_txn["transaction"]
    signatures = real_txn["signatures"]
    message = real_txn["message"]

    # Consolidate loadedAddresses.
    loaded_addresses = models.LoadedAddresses(
        writable=geyser_meta.get("loadedWritableAddresses", []),
        readonly=geyser_meta.get("loadedReadonlyAddresses", []),
    )

    # Geyser doesn't provide blockTime.
    block_time = None

    # Parse instructions using shared helper.
    raw_instructions = message["instructions"]
    instructions: List[models.Instruction] = [shared.instructions(i) for i in raw_instructions]

    # Parse address table lookups if present.
    raw_lookups = message.get("addressTableLookups", [])
    address_table_lookups: List[models.AddressTableLookup] = [shared.address_lookup(lu) for lu in raw_lookups]

    # Normalize program IDs in accountKeys.
    account_keys = shared.program_id(message["accountKeys"])

    # Parse token balances.
    raw_pre_tb = geyser_meta.get("preTokenBalances", [])
    raw_post_tb = geyser_meta.get("postTokenBalances", [])
    pre_token_balances = [shared.token_balance(tb) for tb in raw_pre_tb]
    post_token_balances = [shared.token_balance(tb) for tb in raw_post_tb]

    return models.Transaction(
        slot=slot,
        blockTime=block_time,
        signatures=signatures,
        message=models.Message(
            accountKeys=account_keys,
            recentBlockhash=message["recentBlockhash"],
            instructions=instructions,
            addressTableLookups=address_table_lookups,
        ),
        meta=models.Meta(
            fee=geyser_meta.get("fee", 0),
            preBalances=geyser_meta.get("preBalances", []),
            postBalances=geyser_meta.get("postBalances", []),
            preTokenBalances=pre_token_balances,
            postTokenBalances=post_token_balances,
            innerInstructions=geyser_meta.get("innerInstructions", []),
            logMessages=geyser_meta.get("logMessages", []),
            err=geyser_meta.get("err"),
            status=geyser_meta.get("status", {"Ok": None}),
            computeUnitsConsumed=geyser_meta.get("computeUnitsConsumed"),
        ),
        loadedAddresses=loaded_addresses,
    )
