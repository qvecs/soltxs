from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass(slots=True)
class AddressTableLookup:
    """
    Represents a lookup for an address table in a Solana transaction.

    Attributes:
        accountKey: The account key.
        readonlyIndexes: List of indexes for read-only accounts.
        writableIndexes: List of indexes for writable accounts.
    """

    accountKey: str
    readonlyIndexes: List[int]
    writableIndexes: List[int]


@dataclass(slots=True)
class Instruction:
    """
    Represents a transaction instruction.

    Attributes:
        programIdIndex: Index of the program ID in accountKeys.
        data: Instruction data in base58 encoding.
        accounts: List of account indexes referenced by the instruction.
        stackHeight: Optional stack height for debugging purposes.
    """

    programIdIndex: int
    data: Optional[str]
    accounts: List[int]
    stackHeight: Optional[int]


@dataclass(slots=True)
class Message:
    """
    Represents a transaction message containing instructions and account keys.

    Attributes:
        accountKeys: List of account addresses.
        recentBlockhash: Recent blockhash for the transaction.
        instructions: List of transaction instructions.
        addressTableLookups: List of address table lookups.
    """

    accountKeys: List[str]
    recentBlockhash: str
    instructions: List[Instruction]
    addressTableLookups: List[AddressTableLookup]


@dataclass(slots=True)
class TokenAmount:
    """
    Represents a token amount with associated decimals.

    Attributes:
        amount: Raw token amount as a string.
        decimals: Number of decimals for the token.
        uiAmount: Optional UI-friendly token amount.
        uiAmountString: String representation of the UI amount.
    """

    amount: str
    decimals: int
    uiAmount: Optional[float]
    uiAmountString: str


@dataclass(slots=True)
class TokenBalance:
    """
    Represents a token balance for an account.

    Attributes:
        accountIndex: Index of the account in the transaction.
        mint: Token mint address.
        owner: Token account owner.
        programId: Optional program ID.
        uiTokenAmount: TokenAmount object for the balance.
    """

    accountIndex: int
    mint: str
    owner: str
    programId: Optional[str]
    uiTokenAmount: TokenAmount


@dataclass(slots=True)
class Meta:
    """
    Represents metadata of a transaction.

    Attributes:
        fee: Transaction fee.
        preBalances: Balances before transaction.
        postBalances: Balances after transaction.
        preTokenBalances: List of token balances before transaction.
        postTokenBalances: List of token balances after transaction.
        innerInstructions: List of inner instructions.
        logMessages: Log messages from execution.
        err: Optional error information.
        status: Transaction status.
        computeUnitsConsumed: Optional compute units consumed.
    """

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
    """
    Represents additional loaded addresses (from address lookup tables).

    Attributes:
        writable: List of writable addresses.
        readonly: List of read-only addresses.
    """

    writable: List[str]
    readonly: List[str]


@dataclass(slots=True)
class Transaction:
    """
    Standardized representation of a Solana transaction.

    Attributes:
        slot: Transaction slot.
        blockTime: Optional block time.
        signatures: List of transaction signatures.
        message: Transaction message.
        meta: Transaction metadata.
        loadedAddresses: Loaded addresses from address table lookups.
    """

    slot: int
    blockTime: Optional[int]
    signatures: List[str]
    message: Message
    meta: Meta
    loadedAddresses: LoadedAddresses

    @property
    def all_accounts(self) -> List[str]:
        """
        Returns a unified list of account addresses by combining:
          - message.accountKeys
          - loadedAddresses.writable
          - loadedAddresses.readonly

        Returns:
            List of all account addresses.
        """
        combined = list(self.message.accountKeys)
        combined.extend(self.loadedAddresses.writable)
        combined.extend(self.loadedAddresses.readonly)
        return combined
