import hashlib
from dataclasses import dataclass
from typing import Optional, Union

import qbase58 as base58
import qborsh

from soltxs.normalizer.models import Instruction, Transaction
from soltxs.parser.models import ParsedInstruction, Program

WSOL_MINT = "So11111111111111111111111111111111111111112"
SOL_DECIMALS = 9


@dataclass(slots=True)
class Create(ParsedInstruction):
    """
    Parsed instruction for a PumpFun 'Create' operation.

    Attributes:
        who: Optional creator account.
        mint: Mint account address.
        mint_authority: Mint authority address.
        bonding_curve: Bonding curve address.
        associated_bonding_curve: Associated bonding curve address.
        mpl_token_metadata: Metadata program address.
        metadata: Metadata account address.
        name: Name of the token.
        symbol: Token symbol.
        uri: Token metadata URI.
    """

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
class Swap(ParsedInstruction):
    """
    Parsed instruction for a PumpFun swap operation.

    This simply decodes the raw swap data provided by the program.

    Attributes:
        is_buy: Boolean flag indicating if the swap is a buy.
        sol_amount: Amount in SOL.
        token_amount: Amount of token.
        user: User account address.
        mint: Token mint address.
        timestamp: Timestamp of the operation.
        virtual_sol_reserves: Virtual SOL reserves.
        virtual_token_reserves: Virtual token reserves.
    """

    is_buy: bool
    sol_amount: int
    token_amount: int
    user: str
    mint: str
    timestamp: int
    virtual_sol_reserves: int
    virtual_token_reserves: int


ParsedInstructions = Union[Create, Swap]


@qborsh.schema
class SwapData:
    """
    Borsh schema for swap data in PumpFun operations.

    Attributes:
        mint: Token mint address.
        sol_amount: Amount in SOL.
        token_amount: Amount of token.
        is_buy: Boolean flag indicating a buy operation.
        user: User account address.
        timestamp: Timestamp of the operation.
        virtual_sol_reserves: Virtual SOL reserves.
        virtual_token_reserves: Virtual token reserves.
    """

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
    """
    Borsh schema for create data in PumpFun 'Create' operation.

    Attributes:
        name: Name of the token.
        symbol: Token symbol.
        uri: Token metadata URI.
    """

    name: qborsh.String
    symbol: qborsh.String
    uri: qborsh.String


class _PumpFunParser(Program[ParsedInstructions]):
    """
    Parser for PumpFun program instructions.
    """

    def __init__(self):
        self.program_id = "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"
        self.program_name = "PumpFun"
        calculate_discriminator = lambda x: hashlib.sha256(x.encode("utf-8")).digest()[:8]
        self.desc = lambda d: d[:8]
        self.desc_map = {
            calculate_discriminator("global:buy"): self.parse_Swap,
            calculate_discriminator("global:sell"): self.parse_Swap,
            calculate_discriminator("global:create"): self.parse_Create,
        }

    def parse_Swap(
        self,
        tx: Transaction,
        instruction_index: int,
        decoded_data: bytes,
    ) -> Swap:
        """
        Parses a swap instruction without applying additional business logic.

        Args:
            tx: The Transaction object.
            instruction_index: Index of the instruction.
            decoded_data: Decoded instruction data.

        Returns:
            A Swap parsed instruction containing the raw swap data.
        """
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

        data = result_list[0]
        return Swap(
            program_id=self.program_id,
            program_name=self.program_name,
            instruction_name="Swap",
            is_buy=bool(data["is_buy"]),
            sol_amount=int(data["sol_amount"]),
            token_amount=int(data["token_amount"]),
            user=str(data["user"]),
            mint=str(data["mint"]),
            timestamp=int(data["timestamp"]),
            virtual_sol_reserves=int(data["virtual_sol_reserves"]),
            virtual_token_reserves=int(data["virtual_token_reserves"]),
        )

    def parse_Create(
        self,
        tx: Transaction,
        instruction_index: int,
        decoded_data: bytes,
    ) -> Create:
        """
        Parses a 'Create' instruction.

        Args:
            tx: The Transaction object.
            instruction_index: The index of the instruction.
            decoded_data: Decoded instruction data.

        Returns:
            A Create parsed instruction.
        """
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


PumpFunParser = _PumpFunParser()
