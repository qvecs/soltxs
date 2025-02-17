from dataclasses import asdict

from soltxs import normalize, parse, resolve
from soltxs.parser.parsers.pumpfun import WSOL_MINT


def test_equal_transaction(load_data):
    """
    Test that two PumpFun transactions (Geyser vs RPC) normalize identically.
    """
    tx1 = normalize(load_data("pumpfun_buy_geyser.json"))
    tx2 = normalize(load_data("pumpfun_buy_rpc.json"))

    # Geyser often lacks blockTime; normalize for comparison.
    tx1.blockTime = None
    tx2.blockTime = None
    assert tx1 == tx2


def test_buy_parsing(load_data):
    """
    Ensure PumpFun 'Buy' (now parsed as a Swap) from Geyser or RPC yields matching parse output.
    """
    ge_tx = normalize(load_data("pumpfun_buy_geyser.json"))
    rpc_tx = normalize(load_data("pumpfun_buy_rpc.json"))

    ge_tx.blockTime = None
    rpc_tx.blockTime = None

    ge_parsed = parse(ge_tx)
    rpc_parsed = parse(rpc_tx)

    # Compare top-level fields.
    assert ge_parsed.signatures == rpc_parsed.signatures
    assert ge_parsed.addons == rpc_parsed.addons

    # Now iterate over the parsed instructions.
    for action1, action2 in zip(ge_parsed.instructions, rpc_parsed.instructions):
        d1 = asdict(action1)
        d2 = asdict(action2)
        assert d1 == d2
        if d1.get("program_name") == "PumpFun":
            assert d1["instruction_name"] == "Swap"
            # For a buy transaction, is_buy should be True.
            assert d1["is_buy"] is True
            # The amounts should be greater than 0.
            assert d1["sol_amount"] > 0
            assert d1["token_amount"] > 0


def test_sell_parsing(load_data):
    """
    Confirm that a PumpFun 'Sell' (now parsed as a Swap) transaction parse is correct.
    """
    tx = normalize(load_data("pumpfun_sell_rpc.json"))
    parsed = parse(tx)
    for action in parsed.instructions:
        d = asdict(action)
        if d.get("program_name") == "PumpFun" and d.get("instruction_name") == "Swap":
            # For a sell transaction, is_buy should be False.
            assert d["is_buy"] is False
            assert d["sol_amount"] > 0
            assert d["token_amount"] > 0


def test_resolve_pumpfun_buy(load_data):
    """
    Ensures that resolve(...) identifies a PumpFun 'Buy' instruction.
    """
    tx_data = load_data("pumpfun_buy_rpc.json")
    tx_obj = normalize(tx_data)
    parsed = parse(tx_obj)
    outcome = resolve(parsed)

    assert outcome is not None
    # The resolved type should be 'buy'.
    assert outcome.type == "buy"
    assert outcome.from_token == WSOL_MINT
    assert outcome.from_amount > 0


def test_resolve_pumpfun_sell(load_data):
    """
    Ensures that resolve(...) identifies a PumpFun 'Sell' instruction.
    """
    tx_data = load_data("pumpfun_sell_rpc.json")
    tx_obj = normalize(tx_data)
    parsed = parse(tx_obj)
    outcome = resolve(parsed)

    assert outcome is not None
    # The resolved type should be 'sell'.
    assert outcome.type == "sell"
    assert outcome.to_token == WSOL_MINT
    assert outcome.to_amount > 0


def test_create_parsing(load_data):
    """
    Confirm that a PumpFun 'Create' transaction parse is correct.
    """
    tx = normalize(load_data("pumpfun_create_rpc.json"))
    parsed = parse(tx)
    for action in parsed.instructions:
        d = asdict(action)
        if d.get("program_name") == "PumpFun" and d.get("instruction_name") == "Create":
            assert d["mint"] is not None
            assert d["name"] != ""
            assert d["symbol"] != ""
