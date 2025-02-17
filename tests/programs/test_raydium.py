from dataclasses import asdict

from soltxs import normalize, parse


def test_equal_transaction(load_data):
    """
    Test that two Raydium AMM V4 transactions (Geyser vs RPC) normalize equally.
    """
    geyser_tx = normalize(load_data("raydium_amm_v4_geyser.json"))
    rpc_tx = normalize(load_data("raydium_amm_v4_rpc.json"))

    geyser_tx.blockTime = None
    rpc_tx.blockTime = None
    assert geyser_tx == rpc_tx


def test_parsing(load_data):
    """
    Validate Raydium AMM V4 instructions match for Geyser vs RPC data.
    """
    ge_tx = normalize(load_data("raydium_amm_v4_geyser.json"))
    rpc_tx = normalize(load_data("raydium_amm_v4_rpc.json"))

    ge_parse = parse(ge_tx)
    rpc_parse = parse(rpc_tx)

    # Compare top-level fields.
    assert ge_parse.signatures == rpc_parse.signatures
    assert ge_parse.addons == rpc_parse.addons

    # Iterate over the parsed instructions.
    for g, r in zip(ge_parse.instructions, rpc_parse.instructions):
        dg = asdict(g)
        dr = asdict(r)
        assert dg == dr
        if dg.get("program_name") == "RaydiumAMM":
            assert dg["instruction_name"] == "Swap"
            assert dg["minimum_amount_out"] > 0
