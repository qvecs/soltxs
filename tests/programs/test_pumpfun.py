from dataclasses import asdict
from soltxs import normalize, parse


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
    Ensure PumpFun 'Buy' from Geyser or RPC yields matching parse output.
    """
    ge_tx = normalize(load_data("pumpfun_buy_geyser.json"))
    rpc_tx = normalize(load_data("pumpfun_buy_rpc.json"))

    ge_parsed = parse(ge_tx)
    rpc_parsed = parse(rpc_tx)

    assert ge_parsed == rpc_parsed

    for action1, action2 in zip(ge_parsed, rpc_parsed):
        d1 = asdict(action1)
        d2 = asdict(action2)
        assert d1 == d2
        if d1.get("program_name") == "PumpFun":
            assert d1["instruction_name"] == "Buy"
            assert d1["from_token_amount"] > 0
            assert d1["to_token_amount"] > 0


def test_sell_parsing(load_data):
    """
    Confirm that a PumpFun 'Sell' transaction parse is correct.
    """
    tx = normalize(load_data("pumpfun_sell_rpc.json"))
    parsed = parse(tx)

    for action in parsed:
        a_dict = asdict(action)
        if a_dict.get("program_name") == "PumpFun" and a_dict.get("instruction_name") == "Sell":
            assert a_dict["from_token_amount"] > 0
            assert a_dict["to_token_decimals"] == 9


def test_create_parsing(load_data):
    """
    Confirm that a PumpFun 'Create' transaction parse is correct.
    """
    tx = normalize(load_data("pumpfun_create_rpc.json"))
    parsed = parse(tx)

    for action in parsed:
        a_dict = asdict(action)
        if a_dict.get("program_name") == "PumpFun" and a_dict.get("instruction_name") == "Create":
            assert a_dict["mint"] is not None
            assert a_dict["name"] != ""
            assert a_dict["symbol"] != ""
