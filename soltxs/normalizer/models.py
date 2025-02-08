from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass(slots=True)
class AddressTableLookup:
    accountKey: str
    readonlyIndexes: List[int]
    writableIndexes: List[int]


@dataclass(slots=True)
class Instruction:
    programIdIndex: int
    data: Optional[str]
    accounts: List[int]
    stackHeight: Optional[int]


@dataclass(slots=True)
class Message:
    accountKeys: List[str]
    recentBlockhash: str
    instructions: List[Instruction]
    addressTableLookups: List[AddressTableLookup]


@dataclass(slots=True)
class TokenAmount:
    amount: str
    decimals: int
    uiAmount: Optional[float]
    uiAmountString: str


@dataclass(slots=True)
class TokenBalance:
    accountIndex: int
    mint: str
    owner: str
    programId: Optional[str]
    uiTokenAmount: TokenAmount


@dataclass(slots=True)
class Meta:
    fee: int
    preBalances: List[int]
    postBalances: List[int]
    preTokenBalances: List[TokenBalance]
    postTokenBalances: List[TokenBalance]
    innerInstructions: List[Dict[str, Any]]
    logMessages: List[str]
    err: Optional[Any]
    status: Dict[str, Any]
    computeUnitsConsumed: Optional[int]


@dataclass(slots=True)
class LoadedAddresses:
    writable: List[str]
    readonly: List[str]


@dataclass(slots=True)
class Transaction:
    slot: int
    blockTime: Optional[int]
    signatures: List[str]
    message: Message
    meta: Meta
    loadedAddresses: LoadedAddresses

    @property
    def all_accounts(self) -> List[str]:
        """
        Returns a unified list of account addresses, combining:

          1) message.accountKeys
          2) loadedAddresses.writable
          3) loadedAddresses.readonly

        This is useful for instructions that reference account indices
        beyond the range of message.accountKeys due to address table lookups.
        """
        combined = list(self.message.accountKeys)
        combined.extend(self.loadedAddresses.writable)
        combined.extend(self.loadedAddresses.readonly)
        return combined
