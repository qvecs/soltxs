from typing import List

from soltxs.normalizer.models import (
    AddressTableLookup,
    Instruction,
    TokenAmount,
    TokenBalance,
)


def instructions(instr: dict) -> Instruction:
    return Instruction(
        programIdIndex=instr["programIdIndex"],
        data=instr.get("data", ""),
        accounts=instr.get("accounts", []),
        stackHeight=instr.get("stackHeight", None),
    )


def address_lookup(lookup: dict) -> AddressTableLookup:
    return AddressTableLookup(
        accountKey=lookup["accountKey"],
        readonlyIndexes=lookup.get("readonlyIndexes", []),
        writableIndexes=lookup.get("writableIndexes", []),
    )


def token_balance(tb: dict) -> TokenBalance:
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
