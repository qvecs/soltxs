from dataclasses import dataclass
from typing import Optional, Union

import qborsh

from soltxs.normalizer.models import Instruction, Transaction
from soltxs.parser.models import ParsedInstruction, Program

@dataclass(slots=True)
class CreateAccount(ParsedInstruction):
    funding_account: Optional[str]
    new_account: Optional[str]
    lamports: int
    space: int
    owner: str


@dataclass(slots=True)
class Assign(ParsedInstruction):
    account: Optional[str]
    owner: str


@dataclass(slots=True)
class Transfer(ParsedInstruction):
    from_account: Optional[str]
    to_account: Optional[str]
    lamports: int


@dataclass(slots=True)
class CreateAccountWithSeed(ParsedInstruction):
    funding_account: Optional[str]
    new_account: Optional[str]
    base: str
    seed: str
    lamports: int
    space: int
    owner: str


@dataclass(slots=True)
class AdvanceNonceAccount(ParsedInstruction):
    nonce_account: Optional[str]
    nonce_authority: Optional[str]


@dataclass(slots=True)
class WithdrawNonceAccount(ParsedInstruction):
    nonce_account: Optional[str]
    destination_account: Optional[str]
    nonce_authority: Optional[str]
    lamports: int


@dataclass(slots=True)
class AuthorizeNonceAccount(ParsedInstruction):
    nonce_account: Optional[str]
    nonce_authority: Optional[str]
    new_authority: str


@dataclass(slots=True)
class Allocate(ParsedInstruction):
    account: Optional[str]
    space: int


@dataclass(slots=True)
class AllocateWithSeed(ParsedInstruction):
    account: Optional[str]
    base: str
    seed: str
    space: int
    owner: str


@dataclass(slots=True)
class TransferWithSeed(ParsedInstruction):
    source_account: Optional[str]
    destination_account: Optional[str]
    lamports: int
    seed: str
    owner: str


# Update the union to include all parsed instructions
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
    discriminator: qborsh.Padding[qborsh.U32]
    lamports: qborsh.U64
    space: qborsh.U64
    owner: qborsh.PubKey


@qborsh.schema
class AssignData:
    discriminator: qborsh.Padding[qborsh.U32]
    owner: qborsh.PubKey


@qborsh.schema
class TransferData:
    discriminator: qborsh.Padding[qborsh.U32]
    lamports: qborsh.U64


@qborsh.schema
class CreateAccountWithSeedData:
    discriminator: qborsh.Padding[qborsh.U32]
    base: qborsh.PubKey
    seed: qborsh.String
    lamports: qborsh.U64
    space: qborsh.U64
    owner: qborsh.PubKey


@qborsh.schema
class WithdrawNonceAccountData:
    discriminator: qborsh.Padding[qborsh.U32]
    lamports: qborsh.U64


@qborsh.schema
class AuthorizeNonceAccountData:
    discriminator: qborsh.Padding[qborsh.U32]
    new_authority: qborsh.PubKey


@qborsh.schema
class AllocateData:
    discriminator: qborsh.Padding[qborsh.U32]
    space: qborsh.U64


@qborsh.schema
class AllocateWithSeedData:
    discriminator: qborsh.Padding[qborsh.U32]
    base: qborsh.PubKey
    seed: qborsh.String
    space: qborsh.U64
    owner: qborsh.PubKey


@qborsh.schema
class TransferWithSeedData:
    discriminator: qborsh.Padding[qborsh.U32]
    lamports: qborsh.U64
    seed: qborsh.String
    owner: qborsh.PubKey


class _SystemProgramParser(Program[ParsedInstructions]):
    """
    System Program for account creation, transfers, and more.
    """

    def __init__(self):
        self.program_id = "11111111111111111111111111111111"
        self.program_name = "System Program"
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
        instr: Instruction = tx.message.instructions[instruction_index]
        accounts = instr.accounts
        data = CreateAccountData.decode(decoded_data)
        funding_account = tx.all_accounts[accounts[0]] if len(accounts) > 0 else None
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
        instr: Instruction = tx.message.instructions[instruction_index]
        accounts = instr.accounts
        data = AssignData.decode(decoded_data)
        account = tx.all_accounts[accounts[0]] if len(accounts) > 0 else None
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
        instr: Instruction = tx.message.instructions[instruction_index]
        data = TransferData.decode(decoded_data)
        accounts = instr.accounts
        from_account = tx.all_accounts[accounts[0]] if len(accounts) > 0 else None
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
        instr: Instruction = tx.message.instructions[instruction_index]
        accounts = instr.accounts
        data = CreateAccountWithSeedData.decode(decoded_data)
        funding_account = tx.all_accounts[accounts[0]] if len(accounts) > 0 else None
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
        instr: Instruction = tx.message.instructions[instruction_index]
        accounts = instr.accounts
        nonce_account = tx.all_accounts[accounts[0]] if len(accounts) > 0 else None
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
        instr: Instruction = tx.message.instructions[instruction_index]
        accounts = instr.accounts
        data = WithdrawNonceAccountData.decode(decoded_data)
        nonce_account = tx.all_accounts[accounts[0]] if len(accounts) > 0 else None
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
        instr: Instruction = tx.message.instructions[instruction_index]
        accounts = instr.accounts
        data = AuthorizeNonceAccountData.decode(decoded_data)
        nonce_account = tx.all_accounts[accounts[0]] if len(accounts) > 0 else None
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
        instr: Instruction = tx.message.instructions[instruction_index]
        accounts = instr.accounts
        data = AllocateData.decode(decoded_data)
        account = tx.all_accounts[accounts[0]] if len(accounts) > 0 else None
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
        instr: Instruction = tx.message.instructions[instruction_index]
        accounts = instr.accounts
        data = AllocateWithSeedData.decode(decoded_data)
        account = tx.all_accounts[accounts[0]] if len(accounts) > 0 else None
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
        instr: Instruction = tx.message.instructions[instruction_index]
        accounts = instr.accounts
        data = TransferWithSeedData.decode(decoded_data)
        source_account = tx.all_accounts[accounts[0]] if len(accounts) > 0 else None
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
