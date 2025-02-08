import hashlib
from dataclasses import dataclass
from typing import List, Optional, Union

import qbase58 as base58
import qborsh

from soltxs.normalizer.models import Instruction, Transaction
from soltxs.parser.models import ParsedInstruction, Program

WSOL_MINT = "So11111111111111111111111111111111111111112"
SOL_DECIMALS = 9


@dataclass(slots=True)
class Create(ParsedInstruction):
    who: Optional[str]
    mint: Optional[str]
    mint_authority: Optional[str]
    bonding_curve: Optional[str]
    associated_bonding_curve: Optional[str]
    mpl_token_metadata: Optional[str]
    metadata: Optional[str]
    name: str
    symbol: str
    uri: str


@dataclass(slots=True)
class Buy(ParsedInstruction):
    who: str
    from_token: str
    from_token_decimals: int
    to_token: str
    to_token_decimals: int
    from_token_amount: int
    to_token_amount: int


@dataclass(slots=True)
class Sell(ParsedInstruction):
    who: str
    from_token: str
    from_token_decimals: int
    to_token: str
    to_token_decimals: int
    from_token_amount: int
    to_token_amount: int


ParsedInstructions = Union[Create, Buy, Sell]


@qborsh.schema
class SwapData:
    mint: qborsh.PubKey
    sol_amount: qborsh.U64
    token_amount: qborsh.U64
    is_buy: qborsh.Bool
    user: qborsh.PubKey
    timestamp: qborsh.I64
    virtual_sol_reserves: qborsh.U64
    virtual_token_reserves: qborsh.U64


@qborsh.schema
class CreateData:
    name: qborsh.String
    symbol: qborsh.String
    uri: qborsh.String


class _PumpFunParser(Program[ParsedInstructions]):
    """
    PumpFun parser for handling Buy, Sell, and Create instructions.
    """

    def __init__(self):
        self.program_id = "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"
        self.program_name = "PumpFun"

        calculate_discriminator = lambda x: hashlib.sha256(x.encode("utf-8")).digest()[:8]
        self.desc = lambda d: d[:8]
        self.desc_map = {
            calculate_discriminator("global:buy"): self.parse_Buy,
            calculate_discriminator("global:sell"): self.parse_Sell,
            calculate_discriminator("global:create"): self.parse_Create,
        }

    def parse_Buy(
        self,
        tx: Transaction,
        instruction_index: int,
        decoded_data: bytes,
    ) -> Buy:
        swap_list = self._parse_swap(tx, instruction_index)
        data = swap_list[0]
        from_token = WSOL_MINT
        to_token = str(data["mint"])
        who = str(data["user"])
        from_amount = int(data["sol_amount"])
        to_amount = int(data["token_amount"])
        from_decimals = SOL_DECIMALS
        to_decimals = self._get_token_decimals(tx, to_token)

        return Buy(
            program_id=self.program_id,
            program_name=self.program_name,
            instruction_name="Buy",
            who=who,
            from_token=from_token,
            from_token_decimals=from_decimals,
            to_token=to_token,
            to_token_decimals=to_decimals,
            from_token_amount=from_amount,
            to_token_amount=to_amount,
        )

    def parse_Sell(
        self,
        tx: Transaction,
        instruction_index: int,
        decoded_data: bytes,
    ) -> Sell:
        swap_list = self._parse_swap(tx, instruction_index)
        data = swap_list[0]
        from_token = str(data["mint"])
        to_token = WSOL_MINT
        who = str(data["user"])
        from_amount = int(data["token_amount"])
        to_amount = int(data["sol_amount"])
        from_decimals = self._get_token_decimals(tx, from_token)
        to_decimals = SOL_DECIMALS

        return Sell(
            program_id=self.program_id,
            program_name=self.program_name,
            instruction_name="Sell",
            who=who,
            from_token=from_token,
            from_token_decimals=from_decimals,
            to_token=to_token,
            to_token_decimals=to_decimals,
            from_token_amount=from_amount,
            to_token_amount=to_amount,
        )

    def parse_Create(
        self,
        tx: Transaction,
        instruction_index: int,
        decoded_data: bytes,
    ) -> Create:
        raw = decoded_data[8:]
        create_data = CreateData.decode(raw)
        instr: Instruction = tx.message.instructions[instruction_index]
        who = None
        if len(instr.accounts) > 7:
            who = tx.all_accounts[instr.accounts[7]]
        return Create(
            program_id=self.program_id,
            program_name=self.program_name,
            instruction_name="Create",
            who=who,
            mint=tx.all_accounts[instr.accounts[0]] if len(instr.accounts) > 0 else None,
            mint_authority=tx.all_accounts[instr.accounts[1]] if len(instr.accounts) > 1 else None,
            bonding_curve=tx.all_accounts[instr.accounts[2]] if len(instr.accounts) > 2 else None,
            associated_bonding_curve=tx.all_accounts[instr.accounts[3]] if len(instr.accounts) > 3 else None,
            mpl_token_metadata=tx.all_accounts[instr.accounts[5]] if len(instr.accounts) > 5 else None,
            metadata=tx.all_accounts[instr.accounts[6]] if len(instr.accounts) > 6 else None,
            name=create_data["name"],
            symbol=create_data["symbol"],
            uri=create_data["uri"],
        )

    def _parse_swap(self, tx: Transaction, instruction_index: int) -> List[SwapData]:
        top_instr = tx.message.instructions[instruction_index]
        top_prog_id = tx.all_accounts[top_instr.programIdIndex]

        inner_instrs = []
        for group in tx.meta.innerInstructions:
            if "index" in group:
                if group["index"] == instruction_index:
                    inner_instrs.extend(group["instructions"])
            else:
                inner_instrs.extend(group["instructions"])

        result_list = []
        for in_instr in inner_instrs:
            sub_prog_id = tx.all_accounts[in_instr["programIdIndex"]]
            if sub_prog_id != top_prog_id:
                continue

            raw_data = base58.decode(in_instr.get("data", ""))
            if len(raw_data) < 16:
                continue

            swap_raw = raw_data[16:]
            parsed_obj = SwapData.decode(swap_raw)
            result_list.append(parsed_obj)

        return result_list

    def _get_token_decimals(self, tx: Transaction, mint: str) -> int:
        if mint == WSOL_MINT:
            return SOL_DECIMALS

        for tb in tx.meta.preTokenBalances + tx.meta.postTokenBalances:
            if tb.mint == mint:
                return tb.uiTokenAmount.decimals

        raise ValueError(f"Could not find decimals for mint {mint}")


PumpFunParser = _PumpFunParser()
