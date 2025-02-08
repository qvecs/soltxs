from dataclasses import dataclass
from typing import List, Optional, Union

import qbase58 as base58

from soltxs.normalizer.models import Instruction, Transaction
from soltxs.parser.models import ParsedInstruction, Program


def decode_u64(b: bytes) -> int:
    return int.from_bytes(b, byteorder="little", signed=False)


@dataclass(slots=True)
class InitializeMint(ParsedInstruction):
    decimals: int
    mint_authority: str
    freeze_authority: Optional[str]


@dataclass(slots=True)
class InitializeAccount(ParsedInstruction):
    account: str
    mint: str
    owner: str
    rent_sysvar: str


@dataclass(slots=True)
class InitializeMultisig(ParsedInstruction):
    m: int
    signers: List[str]


@dataclass(slots=True)
class Transfer(ParsedInstruction):
    from_account: str
    to: str
    amount: int


@dataclass(slots=True)
class Approve(ParsedInstruction):
    source: str
    delegate: str
    amount: int


@dataclass(slots=True)
class Revoke(ParsedInstruction):
    source: str


@dataclass(slots=True)
class SetAuthority(ParsedInstruction):
    account: str
    authority_type: int
    new_authority: Optional[str]


@dataclass(slots=True)
class MintTo(ParsedInstruction):
    mint: str
    destination: str
    amount: int


@dataclass(slots=True)
class Burn(ParsedInstruction):
    account: str
    mint: str
    amount: int


@dataclass(slots=True)
class CloseAccount(ParsedInstruction):
    account: str
    destination: str
    authority: str


@dataclass(slots=True)
class FreezeAccount(ParsedInstruction):
    account: str
    mint: str
    freeze_authority: str


@dataclass(slots=True)
class ThawAccount(ParsedInstruction):
    account: str
    mint: str
    freeze_authority: str


@dataclass(slots=True)
class TransferChecked(ParsedInstruction):
    from_account: str
    mint: str
    to: str
    amount: int
    decimals: int


@dataclass(slots=True)
class ApproveChecked(ParsedInstruction):
    source: str
    delegate: str
    amount: int
    decimals: int


@dataclass(slots=True)
class MintToChecked(ParsedInstruction):
    mint: str
    destination: str
    amount: int
    decimals: int


@dataclass(slots=True)
class BurnChecked(ParsedInstruction):
    account: str
    mint: str
    amount: int
    decimals: int


@dataclass(slots=True)
class Unknown(ParsedInstruction):
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
        if custom_accounts is not None:
            accounts = custom_accounts
        else:
            instr: Instruction = tx.message.instructions[instruction_index]
            accounts = instr.accounts
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
        m = decoded_data[1]
        if custom_accounts is not None:
            accounts = custom_accounts
        else:
            instr: Instruction = tx.message.instructions[instruction_index]
            accounts = instr.accounts
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
        if custom_accounts is not None:
            accounts = custom_accounts
        else:
            instr: Instruction = tx.message.instructions[instruction_index]
            accounts = instr.accounts
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
        if custom_accounts is not None:
            accounts = custom_accounts
        else:
            instr: Instruction = tx.message.instructions[instruction_index]
            accounts = instr.accounts
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
        if custom_accounts is not None:
            accounts = custom_accounts
        else:
            instr: Instruction = tx.message.instructions[instruction_index]
            accounts = instr.accounts
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
        authority_type = decoded_data[1]
        option = decoded_data[2]
        new_authority = None
        if option == 1:
            new_authority = base58.encode(decoded_data[3:35]).decode("utf-8")
        if custom_accounts is not None:
            accounts = custom_accounts
        else:
            instr: Instruction = tx.message.instructions[instruction_index]
            accounts = instr.accounts
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
        if custom_accounts is not None:
            accounts = custom_accounts
        else:
            instr: Instruction = tx.message.instructions[instruction_index]
            accounts = instr.accounts
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
        if custom_accounts is not None:
            accounts = custom_accounts
        else:
            instr: Instruction = tx.message.instructions[instruction_index]
            accounts = instr.accounts
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
        if custom_accounts is not None:
            accounts = custom_accounts
        else:
            instr: Instruction = tx.message.instructions[instruction_index]
            accounts = instr.accounts
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
        if custom_accounts is not None:
            accounts = custom_accounts
        else:
            instr: Instruction = tx.message.instructions[instruction_index]
            accounts = instr.accounts
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
        if custom_accounts is not None:
            accounts = custom_accounts
        else:
            instr: Instruction = tx.message.instructions[instruction_index]
            accounts = instr.accounts
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
        if custom_accounts is not None:
            accounts = custom_accounts
        else:
            instr: Instruction = tx.message.instructions[instruction_index]
            accounts = instr.accounts
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
        if custom_accounts is not None:
            accounts = custom_accounts
        else:
            instr: Instruction = tx.message.instructions[instruction_index]
            accounts = instr.accounts
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
        if custom_accounts is not None:
            accounts = custom_accounts
        else:
            instr: Instruction = tx.message.instructions[instruction_index]
            accounts = instr.accounts
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
        if custom_accounts is not None:
            accounts = custom_accounts
        else:
            instr: Instruction = tx.message.instructions[instruction_index]
            accounts = instr.accounts
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
        return Unknown(
            program_id=self.program_id,
            program_name=self.program_name,
            instruction_name="Unknown",
        )

    def _decode_pubkey(self, b: bytes) -> str:
        return base58.encode(b).decode("utf-8")


TokenProgramParser = _TokenProgramParser()
