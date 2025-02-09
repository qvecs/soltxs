from dataclasses import dataclass
from typing import List, Optional, Union

import qbase58 as base58

from soltxs.normalizer.models import Instruction, Transaction
from soltxs.parser.models import ParsedInstruction, Program


def decode_u64(b: bytes) -> int:
    """
    Decodes a little-endian unsigned 64-bit integer from bytes.

    Args:
        b: Bytes to decode.

    Returns:
        The decoded integer.
    """
    return int.from_bytes(b, byteorder="little", signed=False)


@dataclass(slots=True)
class InitializeMint(ParsedInstruction):
    """
    Parsed instruction for initializing a mint.

    Attributes:
        decimals: Number of decimals.
        mint_authority: Mint authority address.
        freeze_authority: Optional freeze authority address.
    """

    decimals: int
    mint_authority: str
    freeze_authority: Optional[str]


@dataclass(slots=True)
class InitializeAccount(ParsedInstruction):
    """
    Parsed instruction for initializing an account.

    Attributes:
        account: The account address.
        mint: Mint address.
        owner: Owner address.
        rent_sysvar: Rent system variable address.
    """

    account: str
    mint: str
    owner: str
    rent_sysvar: str


@dataclass(slots=True)
class InitializeMultisig(ParsedInstruction):
    """
    Parsed instruction for initializing a multisig.

    Attributes:
        m: Required number of signatures.
        signers: List of signer addresses.
    """

    m: int
    signers: List[str]


@dataclass(slots=True)
class Transfer(ParsedInstruction):
    """
    Parsed instruction for transferring tokens.

    Attributes:
        from_account: Source account address.
        to: Destination account address.
        amount: Amount to transfer.
    """

    from_account: str
    to: str
    amount: int


@dataclass(slots=True)
class Approve(ParsedInstruction):
    """
    Parsed instruction for approving token spending.

    Attributes:
        source: Source account address.
        delegate: Delegate account address.
        amount: Amount approved.
    """

    source: str
    delegate: str
    amount: int


@dataclass(slots=True)
class Revoke(ParsedInstruction):
    """
    Parsed instruction for revoking token approval.

    Attributes:
        source: Source account address.
    """

    source: str


@dataclass(slots=True)
class SetAuthority(ParsedInstruction):
    """
    Parsed instruction for setting authority.

    Attributes:
        account: The account address.
        authority_type: Type of authority being set.
        new_authority: Optional new authority address.
    """

    account: str
    authority_type: int
    new_authority: Optional[str]


@dataclass(slots=True)
class MintTo(ParsedInstruction):
    """
    Parsed instruction for minting tokens.

    Attributes:
        mint: Mint address.
        destination: Destination account address.
        amount: Amount to mint.
    """

    mint: str
    destination: str
    amount: int


@dataclass(slots=True)
class Burn(ParsedInstruction):
    """
    Parsed instruction for burning tokens.

    Attributes:
        account: Account address.
        mint: Mint address.
        amount: Amount to burn.
    """

    account: str
    mint: str
    amount: int


@dataclass(slots=True)
class CloseAccount(ParsedInstruction):
    """
    Parsed instruction for closing an account.

    Attributes:
        account: The account address.
        destination: Destination account address.
        authority: Authority address.
    """

    account: str
    destination: str
    authority: str


@dataclass(slots=True)
class FreezeAccount(ParsedInstruction):
    """
    Parsed instruction for freezing an account.

    Attributes:
        account: Account address.
        mint: Mint address.
        freeze_authority: Freeze authority address.
    """

    account: str
    mint: str
    freeze_authority: str


@dataclass(slots=True)
class ThawAccount(ParsedInstruction):
    """
    Parsed instruction for thawing an account.

    Attributes:
        account: Account address.
        mint: Mint address.
        freeze_authority: Freeze authority address.
    """

    account: str
    mint: str
    freeze_authority: str


@dataclass(slots=True)
class TransferChecked(ParsedInstruction):
    """
    Parsed instruction for a checked token transfer.

    Attributes:
        from_account: Source account address.
        mint: Mint address.
        to: Destination account address.
        amount: Amount to transfer.
        decimals: Number of decimals.
    """

    from_account: str
    mint: str
    to: str
    amount: int
    decimals: int


@dataclass(slots=True)
class ApproveChecked(ParsedInstruction):
    """
    Parsed instruction for a checked token approval.

    Attributes:
        source: Source account address.
        delegate: Delegate account address.
        amount: Amount approved.
        decimals: Number of decimals.
    """

    source: str
    delegate: str
    amount: int
    decimals: int


@dataclass(slots=True)
class MintToChecked(ParsedInstruction):
    """
    Parsed instruction for a checked minting operation.

    Attributes:
        mint: Mint address.
        destination: Destination account address.
        amount: Amount to mint.
        decimals: Number of decimals.
    """

    mint: str
    destination: str
    amount: int
    decimals: int


@dataclass(slots=True)
class BurnChecked(ParsedInstruction):
    """
    Parsed instruction for a checked burn operation.

    Attributes:
        account: Account address.
        mint: Mint address.
        amount: Amount to burn.
        decimals: Number of decimals.
    """

    account: str
    mint: str
    amount: int
    decimals: int


@dataclass(slots=True)
class Unknown(ParsedInstruction):
    """
    Parsed instruction for an unknown token program instruction.
    """

    pass


ParsedInstructions = Union[
    InitializeMint,
    InitializeAccount,
    InitializeMultisig,
    Transfer,
    Approve,
    Revoke,
    SetAuthority,
    MintTo,
    Burn,
    CloseAccount,
    FreezeAccount,
    ThawAccount,
    TransferChecked,
    ApproveChecked,
    MintToChecked,
    BurnChecked,
    Unknown,
]


class _TokenProgramParser(Program[ParsedInstructions]):
    """
    Parser for the Token Program instructions.
    """

    def __init__(self):
        self.program_id = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
        self.program_name = "TokenProgram"
        self.desc = lambda d: d[0]
        self.desc_map = {
            0: self.process_InitializeMint,
            1: self.process_InitializeAccount,
            2: self.process_InitializeMultisig,
            3: self.process_Transfer,
            4: self.process_Approve,
            5: self.process_Revoke,
            6: self.process_SetAuthority,
            7: self.process_MintTo,
            8: self.process_Burn,
            9: self.process_CloseAccount,
            10: self.process_FreezeAccount,
            11: self.process_ThawAccount,
            12: self.process_TransferChecked,
            13: self.process_ApproveChecked,
            14: self.process_MintToChecked,
            15: self.process_BurnChecked,
            "default": self.process_Unknown,
        }

    def route_instruction(self, tx: Transaction, instr_dict: dict) -> ParsedInstructions:
        """
        Routes a token program instruction using the discriminator.

        Args:
            tx: The Transaction object.
            instr_dict: The instruction dictionary.

        Returns:
            A parsed token program instruction.
        """
        raw_data = base58.decode(instr_dict.get("data", ""))
        discriminator = self.desc(raw_data)
        parser_func = self.desc_map.get(discriminator, self.desc_map.get("default"))
        return parser_func(
            tx=tx,
            instruction_index=None,
            decoded_data=raw_data,
            custom_accounts=instr_dict["accounts"],
        )

    def process_InitializeMint(
        self,
        tx: Transaction,
        instruction_index: int,
        decoded_data: bytes,
        custom_accounts: Optional[List[int]] = None,
    ) -> InitializeMint:
        """
        Processes an InitializeMint instruction.

        Args:
            tx: The Transaction object.
            instruction_index: Index of the instruction.
            decoded_data: Decoded instruction data.
            custom_accounts: Optional custom account indices.

        Returns:
            An InitializeMint parsed instruction.
        """
        decimals = decoded_data[1]
        mint_authority = base58.encode(decoded_data[2:34]).decode("utf-8")
        option = decoded_data[34]
        freeze_authority = None
        if option == 1:
            freeze_authority = base58.encode(decoded_data[35:67]).decode("utf-8")
        return InitializeMint(
            program_id=self.program_id,
            program_name=self.program_name,
            instruction_name="InitializeMint",
            decimals=decimals,
            mint_authority=mint_authority,
            freeze_authority=freeze_authority,
        )

    def process_InitializeAccount(
        self,
        tx: Transaction,
        instruction_index: int,
        decoded_data: bytes,
        custom_accounts: Optional[List[int]] = None,
    ) -> InitializeAccount:
        """
        Processes an InitializeAccount instruction.

        Args:
            tx: The Transaction object.
            instruction_index: Index of the instruction.
            decoded_data: Decoded instruction data.
            custom_accounts: Optional custom account indices.

        Returns:
            An InitializeAccount parsed instruction.
        """
        accounts = custom_accounts if custom_accounts is not None else tx.message.instructions[instruction_index].accounts
        return InitializeAccount(
            program_id=self.program_id,
            program_name=self.program_name,
            instruction_name="InitializeAccount",
            account=tx.all_accounts[accounts[0]],
            mint=tx.all_accounts[accounts[1]],
            owner=tx.all_accounts[accounts[2]],
            rent_sysvar=tx.all_accounts[accounts[3]],
        )

    def process_InitializeMultisig(
        self,
        tx: Transaction,
        instruction_index: int,
        decoded_data: bytes,
        custom_accounts: Optional[List[int]] = None,
    ) -> InitializeMultisig:
        """
        Processes an InitializeMultisig instruction.

        Args:
            tx: The Transaction object.
            instruction_index: Index of the instruction.
            decoded_data: Decoded instruction data.
            custom_accounts: Optional custom account indices.

        Returns:
            An InitializeMultisig parsed instruction.
        """
        m = decoded_data[1]
        accounts = custom_accounts if custom_accounts is not None else tx.message.instructions[instruction_index].accounts
        signers = [tx.all_accounts[i] for i in accounts]
        return InitializeMultisig(
            program_id=self.program_id,
            program_name=self.program_name,
            instruction_name="InitializeMultisig",
            m=m,
            signers=signers,
        )

    def process_Transfer(
        self,
        tx: Transaction,
        instruction_index: int,
        decoded_data: bytes,
        custom_accounts: Optional[List[int]] = None,
    ) -> Transfer:
        """
        Processes a Transfer instruction.

        Args:
            tx: The Transaction object.
            instruction_index: Index of the instruction.
            decoded_data: Decoded instruction data.
            custom_accounts: Optional custom account indices.

        Returns:
            A Transfer parsed instruction.
        """
        accounts = custom_accounts if custom_accounts is not None else tx.message.instructions[instruction_index].accounts
        amount = decode_u64(decoded_data[1:9])
        return Transfer(
            program_id=self.program_id,
            program_name=self.program_name,
            instruction_name="Transfer",
            from_account=tx.all_accounts[accounts[0]],
            to=tx.all_accounts[accounts[1]],
            amount=amount,
        )

    def process_Approve(
        self,
        tx: Transaction,
        instruction_index: int,
        decoded_data: bytes,
        custom_accounts: Optional[List[int]] = None,
    ) -> Approve:
        """
        Processes an Approve instruction.

        Args:
            tx: The Transaction object.
            instruction_index: Index of the instruction.
            decoded_data: Decoded instruction data.
            custom_accounts: Optional custom account indices.

        Returns:
            An Approve parsed instruction.
        """
        accounts = custom_accounts if custom_accounts is not None else tx.message.instructions[instruction_index].accounts
        amount = decode_u64(decoded_data[1:9])
        return Approve(
            program_id=self.program_id,
            program_name=self.program_name,
            instruction_name="Approve",
            source=tx.all_accounts[accounts[0]],
            delegate=tx.all_accounts[accounts[1]],
            amount=amount,
        )

    def process_Revoke(
        self,
        tx: Transaction,
        instruction_index: int,
        decoded_data: bytes,
        custom_accounts: Optional[List[int]] = None,
    ) -> Revoke:
        """
        Processes a Revoke instruction.

        Args:
            tx: The Transaction object.
            instruction_index: Index of the instruction.
            decoded_data: Decoded instruction data.
            custom_accounts: Optional custom account indices.

        Returns:
            A Revoke parsed instruction.
        """
        accounts = custom_accounts if custom_accounts is not None else tx.message.instructions[instruction_index].accounts
        return Revoke(
            program_id=self.program_id,
            program_name=self.program_name,
            instruction_name="Revoke",
            source=tx.all_accounts[accounts[0]],
        )

    def process_SetAuthority(
        self,
        tx: Transaction,
        instruction_index: int,
        decoded_data: bytes,
        custom_accounts: Optional[List[int]] = None,
    ) -> SetAuthority:
        """
        Processes a SetAuthority instruction.

        Args:
            tx: The Transaction object.
            instruction_index: Index of the instruction.
            decoded_data: Decoded instruction data.
            custom_accounts: Optional custom account indices.

        Returns:
            A SetAuthority parsed instruction.
        """
        authority_type = decoded_data[1]
        option = decoded_data[2]
        new_authority = None
        if option == 1:
            new_authority = base58.encode(decoded_data[3:35]).decode("utf-8")
        accounts = custom_accounts if custom_accounts is not None else tx.message.instructions[instruction_index].accounts
        return SetAuthority(
            program_id=self.program_id,
            program_name=self.program_name,
            instruction_name="SetAuthority",
            account=tx.all_accounts[accounts[0]],
            authority_type=authority_type,
            new_authority=new_authority,
        )

    def process_MintTo(
        self,
        tx: Transaction,
        instruction_index: int,
        decoded_data: bytes,
        custom_accounts: Optional[List[int]] = None,
    ) -> MintTo:
        """
        Processes a MintTo instruction.

        Args:
            tx: The Transaction object.
            instruction_index: Index of the instruction.
            decoded_data: Decoded instruction data.
            custom_accounts: Optional custom account indices.

        Returns:
            A MintTo parsed instruction.
        """
        accounts = custom_accounts if custom_accounts is not None else tx.message.instructions[instruction_index].accounts
        amount = decode_u64(decoded_data[1:9])
        return MintTo(
            program_id=self.program_id,
            program_name=self.program_name,
            instruction_name="MintTo",
            mint=tx.all_accounts[accounts[0]],
            destination=tx.all_accounts[accounts[1]],
            amount=amount,
        )

    def process_Burn(
        self,
        tx: Transaction,
        instruction_index: int,
        decoded_data: bytes,
        custom_accounts: Optional[List[int]] = None,
    ) -> Burn:
        """
        Processes a Burn instruction.

        Args:
            tx: The Transaction object.
            instruction_index: Index of the instruction.
            decoded_data: Decoded instruction data.
            custom_accounts: Optional custom account indices.

        Returns:
            A Burn parsed instruction.
        """
        accounts = custom_accounts if custom_accounts is not None else tx.message.instructions[instruction_index].accounts
        amount = decode_u64(decoded_data[1:9])
        return Burn(
            program_id=self.program_id,
            program_name=self.program_name,
            instruction_name="Burn",
            account=tx.all_accounts[accounts[0]],
            mint=tx.all_accounts[accounts[1]],
            amount=amount,
        )

    def process_CloseAccount(
        self,
        tx: Transaction,
        instruction_index: int,
        decoded_data: bytes,
        custom_accounts: Optional[List[int]] = None,
    ) -> CloseAccount:
        """
        Processes a CloseAccount instruction.

        Args:
            tx: The Transaction object.
            instruction_index: Index of the instruction.
            decoded_data: Decoded instruction data.
            custom_accounts: Optional custom account indices.

        Returns:
            A CloseAccount parsed instruction.
        """
        accounts = custom_accounts if custom_accounts is not None else tx.message.instructions[instruction_index].accounts
        return CloseAccount(
            program_id=self.program_id,
            program_name=self.program_name,
            instruction_name="CloseAccount",
            account=tx.all_accounts[accounts[0]],
            destination=tx.all_accounts[accounts[1]],
            authority=tx.all_accounts[accounts[2]],
        )

    def process_FreezeAccount(
        self,
        tx: Transaction,
        instruction_index: int,
        decoded_data: bytes,
        custom_accounts: Optional[List[int]] = None,
    ) -> FreezeAccount:
        """
        Processes a FreezeAccount instruction.

        Args:
            tx: The Transaction object.
            instruction_index: Index of the instruction.
            decoded_data: Decoded instruction data.
            custom_accounts: Optional custom account indices.

        Returns:
            A FreezeAccount parsed instruction.
        """
        accounts = custom_accounts if custom_accounts is not None else tx.message.instructions[instruction_index].accounts
        return FreezeAccount(
            program_id=self.program_id,
            program_name=self.program_name,
            instruction_name="FreezeAccount",
            account=tx.all_accounts[accounts[0]],
            mint=tx.all_accounts[accounts[1]],
            freeze_authority=tx.all_accounts[accounts[2]],
        )

    def process_ThawAccount(
        self,
        tx: Transaction,
        instruction_index: int,
        decoded_data: bytes,
        custom_accounts: Optional[List[int]] = None,
    ) -> ThawAccount:
        """
        Processes a ThawAccount instruction.

        Args:
            tx: The Transaction object.
            instruction_index: Index of the instruction.
            decoded_data: Decoded instruction data.
            custom_accounts: Optional custom account indices.

        Returns:
            A ThawAccount parsed instruction.
        """
        accounts = custom_accounts if custom_accounts is not None else tx.message.instructions[instruction_index].accounts
        return ThawAccount(
            program_id=self.program_id,
            program_name=self.program_name,
            instruction_name="ThawAccount",
            account=tx.all_accounts[accounts[0]],
            mint=tx.all_accounts[accounts[1]],
            freeze_authority=tx.all_accounts[accounts[2]],
        )

    def process_TransferChecked(
        self,
        tx: Transaction,
        instruction_index: int,
        decoded_data: bytes,
        custom_accounts: Optional[List[int]] = None,
    ) -> TransferChecked:
        """
        Processes a TransferChecked instruction.

        Args:
            tx: The Transaction object.
            instruction_index: Index of the instruction.
            decoded_data: Decoded instruction data.
            custom_accounts: Optional custom account indices.

        Returns:
            A TransferChecked parsed instruction.
        """
        accounts = custom_accounts if custom_accounts is not None else tx.message.instructions[instruction_index].accounts
        amount = decode_u64(decoded_data[1:9])
        decimals = int.from_bytes(decoded_data[9:10], byteorder="little", signed=False)
        return TransferChecked(
            program_id=self.program_id,
            program_name=self.program_name,
            instruction_name="TransferChecked",
            from_account=tx.all_accounts[accounts[0]],
            mint=tx.all_accounts[accounts[1]],
            to=tx.all_accounts[accounts[2]],
            amount=amount,
            decimals=decimals,
        )

    def process_ApproveChecked(
        self,
        tx: Transaction,
        instruction_index: int,
        decoded_data: bytes,
        custom_accounts: Optional[List[int]] = None,
    ) -> ApproveChecked:
        """
        Processes an ApproveChecked instruction.

        Args:
            tx: The Transaction object.
            instruction_index: Index of the instruction.
            decoded_data: Decoded instruction data.
            custom_accounts: Optional custom account indices.

        Returns:
            An ApproveChecked parsed instruction.
        """
        accounts = custom_accounts if custom_accounts is not None else tx.message.instructions[instruction_index].accounts
        amount = decode_u64(decoded_data[1:9])
        decimals = int.from_bytes(decoded_data[9:10], byteorder="little", signed=False)
        return ApproveChecked(
            program_id=self.program_id,
            program_name=self.program_name,
            instruction_name="ApproveChecked",
            source=tx.all_accounts[accounts[0]],
            delegate=tx.all_accounts[accounts[1]],
            amount=amount,
            decimals=decimals,
        )

    def process_MintToChecked(
        self,
        tx: Transaction,
        instruction_index: int,
        decoded_data: bytes,
        custom_accounts: Optional[List[int]] = None,
    ) -> MintToChecked:
        """
        Processes a MintToChecked instruction.

        Args:
            tx: The Transaction object.
            instruction_index: Index of the instruction.
            decoded_data: Decoded instruction data.
            custom_accounts: Optional custom account indices.

        Returns:
            A MintToChecked parsed instruction.
        """
        accounts = custom_accounts if custom_accounts is not None else tx.message.instructions[instruction_index].accounts
        amount = decode_u64(decoded_data[1:9])
        decimals = int.from_bytes(decoded_data[9:10], byteorder="little", signed=False)
        return MintToChecked(
            program_id=self.program_id,
            program_name=self.program_name,
            instruction_name="MintToChecked",
            mint=tx.all_accounts[accounts[0]],
            destination=tx.all_accounts[accounts[1]],
            amount=amount,
            decimals=decimals,
        )

    def process_BurnChecked(
        self,
        tx: Transaction,
        instruction_index: int,
        decoded_data: bytes,
        custom_accounts: Optional[List[int]] = None,
    ) -> BurnChecked:
        """
        Processes a BurnChecked instruction.

        Args:
            tx: The Transaction object.
            instruction_index: Index of the instruction.
            decoded_data: Decoded instruction data.
            custom_accounts: Optional custom account indices.

        Returns:
            A BurnChecked parsed instruction.
        """
        accounts = custom_accounts if custom_accounts is not None else tx.message.instructions[instruction_index].accounts
        amount = decode_u64(decoded_data[1:9])
        decimals = int.from_bytes(decoded_data[9:10], byteorder="little", signed=False)
        return BurnChecked(
            program_id=self.program_id,
            program_name=self.program_name,
            instruction_name="BurnChecked",
            account=tx.all_accounts[accounts[0]],
            mint=tx.all_accounts[accounts[1]],
            amount=amount,
            decimals=decimals,
        )

    def process_Unknown(
        self,
        tx: Transaction,
        instruction_index: int,
        decoded_data: bytes,
        custom_accounts: Optional[List[int]] = None,
    ) -> Unknown:
        """
        Processes an unknown instruction.

        Args:
            tx: The Transaction object.
            instruction_index: Index of the instruction.
            decoded_data: Decoded instruction data.
            custom_accounts: Optional custom account indices.

        Returns:
            An Unknown parsed instruction.
        """
        return Unknown(
            program_id=self.program_id,
            program_name=self.program_name,
            instruction_name="Unknown",
        )

    def _decode_pubkey(self, b: bytes) -> str:
        """
        Decodes a public key from bytes using base58 encoding.

        Args:
            b: Bytes representing the public key.

        Returns:
            The decoded public key as a string.
        """
        return base58.encode(b).decode("utf-8")


TokenProgramParser = _TokenProgramParser()
