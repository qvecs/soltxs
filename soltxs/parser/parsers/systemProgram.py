from dataclasses import dataclass
from typing import Optional, Union

import qborsh

from soltxs.normalizer.models import Instruction, Transaction
from soltxs.parser.models import ParsedInstruction, Program


@dataclass(slots=True)
class CreateAccount(ParsedInstruction):
    """
    Represents a parsed 'CreateAccount' instruction of the System Program.

    Attributes:
        funding_account: The account funding the new account.
        new_account: The newly created account.
        lamports: The number of lamports to transfer.
        space: The amount of space to allocate.
        owner: The program id that will own the new account.
    """

    funding_account: Optional[str]
    new_account: Optional[str]
    lamports: int
    space: int
    owner: str


@dataclass(slots=True)
class Assign(ParsedInstruction):
    """
    Represents a parsed 'Assign' instruction which changes an account's owner.

    Attributes:
        account: The account to be reassigned.
        owner: The new owner program id.
    """

    account: Optional[str]
    owner: str


@dataclass(slots=True)
class Transfer(ParsedInstruction):
    """
    Represents a parsed 'Transfer' instruction for transferring lamports.

    Attributes:
        from_account: The source account.
        to_account: The destination account.
        lamports: The amount of lamports to transfer.
    """

    from_account: Optional[str]
    to_account: Optional[str]
    lamports: int


@dataclass(slots=True)
class CreateAccountWithSeed(ParsedInstruction):
    """
    Represents a parsed 'CreateAccountWithSeed' instruction.

    Attributes:
        funding_account: The account funding the new account.
        new_account: The new account being created.
        base: The base account used for seed derivation.
        seed: The seed string.
        lamports: The number of lamports to fund the new account.
        space: The allocated space for the new account.
        owner: The program id that will own the new account.
    """

    funding_account: Optional[str]
    new_account: Optional[str]
    base: str
    seed: str
    lamports: int
    space: int
    owner: str


@dataclass(slots=True)
class AdvanceNonceAccount(ParsedInstruction):
    """
    Represents a parsed 'AdvanceNonceAccount' instruction.

    Attributes:
        nonce_account: The nonce account to advance.
        nonce_authority: The authority that can advance the nonce.
    """

    nonce_account: Optional[str]
    nonce_authority: Optional[str]


@dataclass(slots=True)
class WithdrawNonceAccount(ParsedInstruction):
    """
    Represents a parsed 'WithdrawNonceAccount' instruction.

    Attributes:
        nonce_account: The nonce account to withdraw from.
        destination_account: The account to receive the withdrawn lamports.
        nonce_authority: The authority of the nonce account.
        lamports: The amount of lamports to withdraw.
    """

    nonce_account: Optional[str]
    destination_account: Optional[str]
    nonce_authority: Optional[str]
    lamports: int


@dataclass(slots=True)
class AuthorizeNonceAccount(ParsedInstruction):
    """
    Represents a parsed 'AuthorizeNonceAccount' instruction.

    Attributes:
        nonce_account: The nonce account.
        nonce_authority: The current nonce authority.
        new_authority: The new authority to be assigned.
    """

    nonce_account: Optional[str]
    nonce_authority: Optional[str]
    new_authority: str


@dataclass(slots=True)
class Allocate(ParsedInstruction):
    """
    Represents a parsed 'Allocate' instruction which allocates space for an account.

    Attributes:
        account: The account to allocate space for.
        space: The amount of space to allocate.
    """

    account: Optional[str]
    space: int


@dataclass(slots=True)
class AllocateWithSeed(ParsedInstruction):
    """
    Represents a parsed 'AllocateWithSeed' instruction.

    Attributes:
        account: The account to allocate space for.
        base: The base account used for seed derivation.
        seed: The seed string.
        space: The amount of space to allocate.
        owner: The program id that will own the account.
    """

    account: Optional[str]
    base: str
    seed: str
    space: int
    owner: str


@dataclass(slots=True)
class TransferWithSeed(ParsedInstruction):
    """
    Represents a parsed 'TransferWithSeed' instruction.

    Attributes:
        source_account: The source account.
        destination_account: The destination account.
        lamports: The amount of lamports to transfer.
        seed: The seed string used in derivation.
        owner: The owner program id.
    """

    source_account: Optional[str]
    destination_account: Optional[str]
    lamports: int
    seed: str
    owner: str


# Union of all parsed instructions for the System Program.
ParsedInstructions = Union[
    CreateAccount,
    Assign,
    Transfer,
    CreateAccountWithSeed,
    AdvanceNonceAccount,
    WithdrawNonceAccount,
    AuthorizeNonceAccount,
    Allocate,
    AllocateWithSeed,
    TransferWithSeed,
]


@qborsh.schema
class CreateAccountData:
    """
    Borsh schema for CreateAccount instruction data.

    Attributes:
        discriminator: A 4-byte padding discriminator.
        lamports: Number of lamports to fund.
        space: Space to allocate.
        owner: The owner program id.
    """

    discriminator: qborsh.Padding[qborsh.U32]
    lamports: qborsh.U64
    space: qborsh.U64
    owner: qborsh.PubKey


@qborsh.schema
class AssignData:
    """
    Borsh schema for Assign instruction data.

    Attributes:
        discriminator: A 4-byte padding discriminator.
        owner: The new owner program id.
    """

    discriminator: qborsh.Padding[qborsh.U32]
    owner: qborsh.PubKey


@qborsh.schema
class TransferData:
    """
    Borsh schema for Transfer instruction data.

    Attributes:
        discriminator: A 4-byte padding discriminator.
        lamports: The amount of lamports to transfer.
    """

    discriminator: qborsh.Padding[qborsh.U32]
    lamports: qborsh.U64


@qborsh.schema
class CreateAccountWithSeedData:
    """
    Borsh schema for CreateAccountWithSeed instruction data.

    Attributes:
        discriminator: A 4-byte padding discriminator.
        base: The base account for seed derivation.
        seed: The seed string.
        lamports: The number of lamports to fund.
        space: The space to allocate.
        owner: The owner program id.
    """

    discriminator: qborsh.Padding[qborsh.U32]
    base: qborsh.PubKey
    seed: qborsh.String
    lamports: qborsh.U64
    space: qborsh.U64
    owner: qborsh.PubKey


@qborsh.schema
class WithdrawNonceAccountData:
    """
    Borsh schema for WithdrawNonceAccount instruction data.

    Attributes:
        discriminator: A 4-byte padding discriminator.
        lamports: The amount to withdraw.
    """

    discriminator: qborsh.Padding[qborsh.U32]
    lamports: qborsh.U64


@qborsh.schema
class AuthorizeNonceAccountData:
    """
    Borsh schema for AuthorizeNonceAccount instruction data.

    Attributes:
        discriminator: A 4-byte padding discriminator.
        new_authority: The new authority for the nonce account.
    """

    discriminator: qborsh.Padding[qborsh.U32]
    new_authority: qborsh.PubKey


@qborsh.schema
class AllocateData:
    """
    Borsh schema for Allocate instruction data.

    Attributes:
        discriminator: A 4-byte padding discriminator.
        space: The space to allocate.
    """

    discriminator: qborsh.Padding[qborsh.U32]
    space: qborsh.U64


@qborsh.schema
class AllocateWithSeedData:
    """
    Borsh schema for AllocateWithSeed instruction data.

    Attributes:
        discriminator: A 4-byte padding discriminator.
        base: The base account for seed derivation.
        seed: The seed string.
        space: The space to allocate.
        owner: The owner program id.
    """

    discriminator: qborsh.Padding[qborsh.U32]
    base: qborsh.PubKey
    seed: qborsh.String
    space: qborsh.U64
    owner: qborsh.PubKey


@qborsh.schema
class TransferWithSeedData:
    """
    Borsh schema for TransferWithSeed instruction data.

    Attributes:
        discriminator: A 4-byte padding discriminator.
        lamports: The amount to transfer.
        seed: The seed string.
        owner: The owner program id.
    """

    discriminator: qborsh.Padding[qborsh.U32]
    lamports: qborsh.U64
    seed: qborsh.String
    owner: qborsh.PubKey


class _SystemProgramParser(Program[ParsedInstructions]):
    """
    Parser for the Solana System Program instructions which include account creation,
    transfers, nonce account operations, and allocation instructions.
    """

    def __init__(self):
        self.program_id = "11111111111111111111111111111111"
        self.program_name = "System Program"
        # The first 4 bytes of instruction data serve as the discriminator.
        self.desc = lambda d: int.from_bytes(d[0:4], byteorder="little", signed=False)
        self.desc_map = {
            0: self.process_CreateAccount,
            1: self.process_Assign,
            2: self.process_Transfer,
            3: self.process_CreateAccountWithSeed,
            4: self.process_AdvanceNonceAccount,
            5: self.process_WithdrawNonceAccount,
            6: self.process_AuthorizeNonceAccount,
            7: self.process_Allocate,
            8: self.process_AllocateWithSeed,
            9: self.process_TransferWithSeed,
        }

    def process_CreateAccount(
        self,
        tx: Transaction,
        instruction_index: int,
        decoded_data: bytes,
    ) -> CreateAccount:
        """
        Processes a CreateAccount instruction.

        Args:
            tx: The transaction object.
            instruction_index: The index of the instruction within the transaction.
            decoded_data: The decoded instruction data.

        Returns:
            A CreateAccount parsed instruction.
        """
        instr: Instruction = tx.message.instructions[instruction_index]
        accounts = instr.accounts
        data = CreateAccountData.decode(decoded_data)
        funding_account = tx.all_accounts[accounts[0]] if accounts else None
        new_account = tx.all_accounts[accounts[1]] if len(accounts) > 1 else None
        return CreateAccount(
            program_id=self.program_id,
            program_name=self.program_name,
            instruction_name="CreateAccount",
            funding_account=funding_account,
            new_account=new_account,
            lamports=int(data["lamports"]),
            space=int(data["space"]),
            owner=data["owner"],
        )

    def process_Assign(
        self,
        tx: Transaction,
        instruction_index: int,
        decoded_data: bytes,
    ) -> Assign:
        """
        Processes an Assign instruction.

        Args:
            tx: The transaction object.
            instruction_index: The index of the instruction.
            decoded_data: The decoded instruction data.

        Returns:
            An Assign parsed instruction.
        """
        instr: Instruction = tx.message.instructions[instruction_index]
        accounts = instr.accounts
        data = AssignData.decode(decoded_data)
        account = tx.all_accounts[accounts[0]] if accounts else None
        return Assign(
            program_id=self.program_id,
            program_name=self.program_name,
            instruction_name="Assign",
            account=account,
            owner=data["owner"],
        )

    def process_Transfer(
        self,
        tx: Transaction,
        instruction_index: int,
        decoded_data: bytes,
    ) -> Transfer:
        """
        Processes a Transfer instruction.

        Args:
            tx: The transaction object.
            instruction_index: The index of the instruction.
            decoded_data: The decoded instruction data.

        Returns:
            A Transfer parsed instruction.
        """
        instr: Instruction = tx.message.instructions[instruction_index]
        data = TransferData.decode(decoded_data)
        accounts = instr.accounts
        from_account = tx.all_accounts[accounts[0]] if accounts else None
        to_account = tx.all_accounts[accounts[1]] if len(accounts) > 1 else None
        return Transfer(
            program_id=self.program_id,
            program_name=self.program_name,
            instruction_name="Transfer",
            from_account=from_account,
            to_account=to_account,
            lamports=int(data["lamports"]),
        )

    def process_CreateAccountWithSeed(
        self,
        tx: Transaction,
        instruction_index: int,
        decoded_data: bytes,
    ) -> CreateAccountWithSeed:
        """
        Processes a CreateAccountWithSeed instruction.

        Args:
            tx: The transaction object.
            instruction_index: The index of the instruction.
            decoded_data: The decoded instruction data.

        Returns:
            A CreateAccountWithSeed parsed instruction.
        """
        instr: Instruction = tx.message.instructions[instruction_index]
        accounts = instr.accounts
        data = CreateAccountWithSeedData.decode(decoded_data)
        funding_account = tx.all_accounts[accounts[0]] if accounts else None
        new_account = tx.all_accounts[accounts[1]] if len(accounts) > 1 else None
        return CreateAccountWithSeed(
            program_id=self.program_id,
            program_name=self.program_name,
            instruction_name="CreateAccountWithSeed",
            funding_account=funding_account,
            new_account=new_account,
            base=data["base"],
            seed=data["seed"],
            lamports=int(data["lamports"]),
            space=int(data["space"]),
            owner=data["owner"],
        )

    def process_AdvanceNonceAccount(
        self,
        tx: Transaction,
        instruction_index: int,
        decoded_data: bytes,
    ) -> AdvanceNonceAccount:
        """
        Processes an AdvanceNonceAccount instruction.

        Args:
            tx: The transaction object.
            instruction_index: The index of the instruction.
            decoded_data: The decoded instruction data.

        Returns:
            An AdvanceNonceAccount parsed instruction.
        """
        instr: Instruction = tx.message.instructions[instruction_index]
        accounts = instr.accounts
        nonce_account = tx.all_accounts[accounts[0]] if accounts else None
        nonce_authority = tx.all_accounts[accounts[1]] if len(accounts) > 1 else None
        return AdvanceNonceAccount(
            program_id=self.program_id,
            program_name=self.program_name,
            instruction_name="AdvanceNonceAccount",
            nonce_account=nonce_account,
            nonce_authority=nonce_authority,
        )

    def process_WithdrawNonceAccount(
        self,
        tx: Transaction,
        instruction_index: int,
        decoded_data: bytes,
    ) -> WithdrawNonceAccount:
        """
        Processes a WithdrawNonceAccount instruction.

        Args:
            tx: The transaction object.
            instruction_index: The index of the instruction.
            decoded_data: The decoded instruction data.

        Returns:
            A WithdrawNonceAccount parsed instruction.
        """
        instr: Instruction = tx.message.instructions[instruction_index]
        accounts = instr.accounts
        data = WithdrawNonceAccountData.decode(decoded_data)
        nonce_account = tx.all_accounts[accounts[0]] if accounts else None
        destination_account = tx.all_accounts[accounts[1]] if len(accounts) > 1 else None
        nonce_authority = tx.all_accounts[accounts[2]] if len(accounts) > 2 else None
        return WithdrawNonceAccount(
            program_id=self.program_id,
            program_name=self.program_name,
            instruction_name="WithdrawNonceAccount",
            nonce_account=nonce_account,
            destination_account=destination_account,
            nonce_authority=nonce_authority,
            lamports=int(data["lamports"]),
        )

    def process_AuthorizeNonceAccount(
        self,
        tx: Transaction,
        instruction_index: int,
        decoded_data: bytes,
    ) -> AuthorizeNonceAccount:
        """
        Processes an AuthorizeNonceAccount instruction.

        Args:
            tx: The transaction object.
            instruction_index: The index of the instruction.
            decoded_data: The decoded instruction data.

        Returns:
            An AuthorizeNonceAccount parsed instruction.
        """
        instr: Instruction = tx.message.instructions[instruction_index]
        accounts = instr.accounts
        data = AuthorizeNonceAccountData.decode(decoded_data)
        nonce_account = tx.all_accounts[accounts[0]] if accounts else None
        nonce_authority = tx.all_accounts[accounts[1]] if len(accounts) > 1 else None
        return AuthorizeNonceAccount(
            program_id=self.program_id,
            program_name=self.program_name,
            instruction_name="AuthorizeNonceAccount",
            nonce_account=nonce_account,
            nonce_authority=nonce_authority,
            new_authority=data["new_authority"],
        )

    def process_Allocate(
        self,
        tx: Transaction,
        instruction_index: int,
        decoded_data: bytes,
    ) -> Allocate:
        """
        Processes an Allocate instruction.

        Args:
            tx: The transaction object.
            instruction_index: The index of the instruction.
            decoded_data: The decoded instruction data.

        Returns:
            An Allocate parsed instruction.
        """
        instr: Instruction = tx.message.instructions[instruction_index]
        accounts = instr.accounts
        data = AllocateData.decode(decoded_data)
        account = tx.all_accounts[accounts[0]] if accounts else None
        return Allocate(
            program_id=self.program_id,
            program_name=self.program_name,
            instruction_name="Allocate",
            account=account,
            space=int(data["space"]),
        )

    def process_AllocateWithSeed(
        self,
        tx: Transaction,
        instruction_index: int,
        decoded_data: bytes,
    ) -> AllocateWithSeed:
        """
        Processes an AllocateWithSeed instruction.

        Args:
            tx: The transaction object.
            instruction_index: The index of the instruction.
            decoded_data: The decoded instruction data.

        Returns:
            An AllocateWithSeed parsed instruction.
        """
        instr: Instruction = tx.message.instructions[instruction_index]
        accounts = instr.accounts
        data = AllocateWithSeedData.decode(decoded_data)
        account = tx.all_accounts[accounts[0]] if accounts else None
        return AllocateWithSeed(
            program_id=self.program_id,
            program_name=self.program_name,
            instruction_name="AllocateWithSeed",
            account=account,
            base=data["base"],
            seed=data["seed"],
            space=int(data["space"]),
            owner=data["owner"],
        )

    def process_TransferWithSeed(
        self,
        tx: Transaction,
        instruction_index: int,
        decoded_data: bytes,
    ) -> TransferWithSeed:
        """
        Processes a TransferWithSeed instruction.

        Args:
            tx: The transaction object.
            instruction_index: The index of the instruction.
            decoded_data: The decoded instruction data.

        Returns:
            A TransferWithSeed parsed instruction.
        """
        instr: Instruction = tx.message.instructions[instruction_index]
        accounts = instr.accounts
        data = TransferWithSeedData.decode(decoded_data)
        source_account = tx.all_accounts[accounts[0]] if accounts else None
        # For TransferWithSeed, the destination account is expected to be at index 2.
        destination_account = tx.all_accounts[accounts[2]] if len(accounts) > 2 else None
        return TransferWithSeed(
            program_id=self.program_id,
            program_name=self.program_name,
            instruction_name="TransferWithSeed",
            source_account=source_account,
            destination_account=destination_account,
            lamports=int(data["lamports"]),
            seed=data["seed"],
            owner=data["owner"],
        )


SystemProgramParser = _SystemProgramParser()
