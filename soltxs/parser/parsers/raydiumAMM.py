from dataclasses import dataclass
from typing import Union

import qbase58 as base58

from soltxs.normalizer.models import Instruction, Transaction
from soltxs.parser.models import ParsedInstruction, Program
from soltxs.parser.parsers.tokenProgram import TokenProgramParser

WSOL_MINT = "So11111111111111111111111111111111111111112"
SOL_DECIMALS = 9


@dataclass(slots=True)
class Swap(ParsedInstruction):
    who: str
    from_token: str
    from_token_amount: int
    from_token_decimals: int
    to_token: str
    to_token_amount: int
    to_token_decimals: int
    minimum_amount_out: int


ParsedInstructions = Union[Swap]


class _RaydiumAMMParser(Program[ParsedInstructions]):
    """
    Raydium's AMM v4 program for token swaps.
    """

    def __init__(self):
        self.program_id = "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8"
        self.program_name = "RaydiumAMM"

        self.desc = lambda d: d[0]
        self.desc_map = {9: self.process_Swap}

    def process_Swap(
        self,
        tx: Transaction,
        instruction_index: int,
        decoded_data: bytes,
    ) -> Swap:
        # Retrieve the original instruction from the transaction message.
        instr: Instruction = tx.message.instructions[instruction_index]
        accounts = instr.accounts

        # Safely decode the instruction data in case it is missing.
        decoded_data = base58.decode(instr.data or "")
        amount_in = int.from_bytes(decoded_data[1:9], byteorder="little", signed=False)
        minimum_amount_out = int.from_bytes(decoded_data[9:17], byteorder="little", signed=False)

        user_source = tx.all_accounts[accounts[len(accounts) - 3]]
        user_destination = tx.all_accounts[accounts[len(accounts) - 2]]
        who = tx.all_accounts[accounts[len(accounts) - 1]]

        from_token = WSOL_MINT
        from_token_decimals = SOL_DECIMALS
        to_token = WSOL_MINT
        to_token_decimals = SOL_DECIMALS

        # Consolidate token balances from pre and post token balances.
        combined_tb = []
        combined_tb.extend(tx.meta.preTokenBalances)
        combined_tb.extend(tx.meta.postTokenBalances)

        for tb in combined_tb:
            token_account = tx.all_accounts[tb.accountIndex]
            if token_account == user_source:
                from_token = tb.mint
                from_token_decimals = tb.uiTokenAmount.decimals
            elif token_account == user_destination:
                to_token = tb.mint
                to_token_decimals = tb.uiTokenAmount.decimals

        to_token_amount = 0
        inner_instrs = []
        # Search for inner instructions corresponding to the current instruction index.
        for i_group in tx.meta.innerInstructions:
            if i_group["index"] == instruction_index:
                inner_instrs.extend(i_group["instructions"])
                break

        # Process inner instructions for token transfers.
        for in_instr in inner_instrs:
            program_id = tx.all_accounts[in_instr["programIdIndex"]]
            if program_id == TokenProgramParser.program_id:
                action = TokenProgramParser.route_instruction(tx, in_instr)
                if action.instruction_name in ["Transfer", "TransferChecked"] and action.to == user_destination:
                    to_token_amount = action.amount

        return Swap(
            program_id=self.program_id,
            program_name=self.program_name,
            instruction_name="Swap",
            who=who,
            from_token=from_token,
            from_token_amount=amount_in,
            from_token_decimals=from_token_decimals,
            to_token=to_token,
            to_token_amount=to_token_amount,
            to_token_decimals=to_token_decimals,
            minimum_amount_out=minimum_amount_out,
        )


RaydiumAMMParser = _RaydiumAMMParser()
