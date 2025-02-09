# 📟 Solana Transactions _(soltxs)_

Solana transaction normalizer, parser, and resolver.

## Installing

```bash
pip install soltxs
```

## Overview

This library breaks down Solana transaction introspection and analysis into three steps: 

1. **Normalize**: Converts a raw JSON RPC payload into a `Transaction` object.
2. **Parse**: Routes each instruction in the `Transaction` to the correct program-level parser. Produces objects describing each recognized instruction.
3. **Resolve**: Takes the parsed instructions and converts them into a more human-readable format.

#### Support 

* Normalizers
    * Standard RPC Response
    * Modified YellowStone Geyser Response
* Parsers
    * Compute Budget
    * System Program
    * Token Program
    * PumpFun Program
    * Raydium AMM Program
* Resolvers
    * PumpFun Swap
    * Raydium Swap

## Usage

```python
import soltxs

tx = {"jsonrpc": ..., "result": ..., "id": ...}

# All three steps below can be combined into a single call.
# Equivalent to: resolve(parse(normalize(tx)))
result = soltxs.process(tx)

norm_tx = soltxs.normalize(tx)
# Transaction(
#     slot=...,
#     blockTime=...,
#     signatures=[...],
#     message=...,
#     meta=...,
#     loadedAddresses=...,
# )

parsed_data = soltxs.parse(norm_tx)
# {
#     "signatures": [...],
#     "instructions": [
#         <ComputeBudget.SetComputeUnitLimit(...)>,
#         <ComputeBudget.SetComputeUnitPrice(...)>,
#         <SystemProgram.CreateAccount(...)>,
#         <TokenProgram.InitAccount(...)>,
#         <RaydiumAMM.Swap(...)>,
#         <TokenProgram.Unknown(...)>,
#         <SystemProgram.Transfer(...)>,
#         <UnknownProgram.Unknown(...)>,
#     ],
#     "addons": {
#         {"compute_units": <ComputeUnits(...)>},
#         {"instruction_count": <InstructionCount(...)>},
#         {"loaded_addresses": <LoadedAddresses(...)>},
#         {"platform_identifier": <PlatformIdentifier(...)>},
#         {"token_transfer_summary": <TokenTransfer(...)>}
#     }
# }

resolved_tx = soltxs.resolve(parsed_data)
# For example, a Raydium resolved output might be:
# Raydium(
#     type=...,
#     who=...,
#     from_token=...,
#     from_amount=...,
#     to_token=...,
#     to_amount=...,
#     minimum_amount_out=...
# )
```
