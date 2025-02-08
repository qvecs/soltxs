from collections import defaultdict
from dataclasses import dataclass
from typing import List, Optional, Union

import qbase58 as base58

from soltxs.normalizer.models import Instruction, Transaction
from soltxs.parser.models import ParsedInstruction, Program


@dataclass(slots=True)
class InitAccount(ParsedInstruction):
    account: str
    mint: str
    owner: str
    rent_sysvar: str


@dataclass(slots=True)
class Transfer(ParsedInstruction):
    from_account: str
    to: str
    amount: int


@dataclass(slots=True)
class TransferChecked(ParsedInstruction):
    from_account: str
    mint: str
    to: str
    amount: int
    decimals: int


@dataclass(slots=True)
class Unknown(ParsedInstruction):
    pass


ParsedInstructions = Union[InitAccount, Transfer, TransferChecked, Unknown]


class _TokenProgramParser(Program[ParsedInstructions]):
    def __init__(self):
        self.program_id = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
        self.program_name = "TokenProgram"

        self.desc = lambda d: d[0]
        self.desc_map = {
            1: self.process_InitAccount,
            3: self.process_Transfer,
            12: self.process_TransferChecked,
            "default": self.process_Unknown,
        }

    def route_instruction(self, tx: Transaction, instr_dict: dict) -> ParsedInstructions:
        raw_data = base58.decode(instr_dict["data"])
        descriminator = self.desc(raw_data)
        parser_func = self.desc_map.get(descriminator, self.desc_map.get("default"))
        return parser_func(
            tx=tx,
            instruction_index=None,
            decoded_data=raw_data,
            custom_accounts=instr_dict["accounts"],
        )

    def process_InitAccount(
        self,
        tx: Transaction,
        instruction_index: int,
        decoded_data: bytes,
        custom_accounts: list[int] = None,
    ) -> InitAccount:
        if custom_accounts is not None:
            accounts = custom_accounts
        else:
            instr: Instruction = tx.message.instructions[instruction_index]
            accounts = instr.accounts

        account = tx.all_accounts[accounts[0]]
        mint = tx.all_accounts[accounts[1]]
        owner = tx.all_accounts[accounts[2]]
        rent_sysvar = tx.all_accounts[accounts[3]]

        return InitAccount(
            program_id=self.program_id,
            program_name=self.program_name,
            instruction_name="InitializeAccount",
            account=account,
            mint=mint,
            owner=owner,
            rent_sysvar=rent_sysvar,
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
            instr = None
        else:
            instr = tx.message.instructions[instruction_index]
            accounts = instr.accounts

        return Transfer(
            program_id=self.program_id,
            program_name=self.program_name,
            instruction_name="Transfer",
            from_account=tx.all_accounts[accounts[0]],
            to=tx.all_accounts[accounts[1]],
            amount=int.from_bytes(decoded_data[1:9], byteorder="little", signed=False),
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

        return TransferChecked(
            program_id=self.program_id,
            program_name=self.program_name,
            instruction_name="TransferChecked",
            from_account=tx.all_accounts[accounts[0]],
            mint=tx.all_accounts[accounts[1]],
            to=tx.all_accounts[accounts[2]],
            amount=int.from_bytes(decoded_data[1:9], byteorder="little", signed=False),
            decimals=int.from_bytes(decoded_data[9:17], byteorder="little", signed=False),
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


TokenProgramParser = _TokenProgramParser()
