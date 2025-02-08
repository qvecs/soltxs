from typing import List

from soltxs.normalizer.models import (
    AddressTableLookup,
    Instruction,
    TokenAmount,
    TokenBalance,
)


def instructions(instr: dict) -> Instruction:
    """
    Converts a raw instruction dictionary to an Instruction object.

    Args:
        instr: The raw instruction dictionary.

    Returns:
        An Instruction object.
    """
    return Instruction(
        programIdIndex=instr["programIdIndex"],
        data=instr.get("data", ""),
        accounts=instr.get("accounts", []),
        stackHeight=instr.get("stackHeight", None),
    )


def address_lookup(lookup: dict) -> AddressTableLookup:
    """
    Converts a raw address lookup dictionary to an AddressTableLookup object.

    Args:
        lookup: The raw lookup dictionary.

    Returns:
        An AddressTableLookup object.
    """
    return AddressTableLookup(
        accountKey=lookup["accountKey"],
        readonlyIndexes=lookup.get("readonlyIndexes", []),
        writableIndexes=lookup.get("writableIndexes", []),
    )


def token_balance(tb: dict) -> TokenBalance:
    """
    Converts a raw token balance dictionary to a TokenBalance object.

    Args:
        tb: The raw token balance dictionary.

    Returns:
        A TokenBalance object.
    """
    return TokenBalance(
        accountIndex=tb["accountIndex"],
        mint=tb["mint"],
        owner=tb["owner"],
        programId=tb.get("programId"),
        uiTokenAmount=TokenAmount(
            amount=tb["uiTokenAmount"]["amount"],
            decimals=tb["uiTokenAmount"]["decimals"],
            uiAmount=tb["uiTokenAmount"].get("uiAmount"),
            uiAmountString=tb["uiTokenAmount"]["uiAmountString"],
        ),
    )


def program_id(keys: List[str]) -> List[str]:
    """
    Convert any 33-ones key to 32-ones for consistency.

    Args:
        keys: List of program keys.

    Returns:
        List of program keys with 33-ones key converted to 32-ones.
    """
    unified = []
    for k in keys:
        if k == "111111111111111111111111111111111":
            unified.append("11111111111111111111111111111111")
        else:
            unified.append(k)
    return unified
