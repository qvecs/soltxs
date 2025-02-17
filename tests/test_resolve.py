from soltxs import normalize, parse, resolve
from soltxs.resolver.models import Resolve


def test_resolve_pumpfun_buy(load_data):
    """
    Ensures that resolve(...) identifies a PumpFun 'Buy' instruction.
    """
    tx_data = load_data("pumpfun_buy_rpc.json")
    tx_obj = normalize(tx_data)
    parsed = parse(tx_obj)
    outcome = resolve(parsed)

    assert isinstance(outcome, Resolve)
    assert getattr(outcome, "type", None) == "buy"
    assert getattr(outcome, "from_amount", 0) > 0


def test_resolve_pumpfun_sell(load_data):
    """
    Ensures that resolve(...) identifies a PumpFun 'Sell' instruction.
    """
    tx_data = load_data("pumpfun_sell_rpc.json")
    tx_obj = normalize(tx_data)
    parsed = parse(tx_obj)
    outcome = resolve(parsed)

    assert getattr(outcome, "type", None) == "sell"
    assert getattr(outcome, "to_amount", 0) > 0


def test_resolve_raydium_swap(load_data):
    """
    Ensures that a Raydium V4 'Swap' is resolved properly.
    """
    tx_data = load_data("raydium_amm_v4_rpc.json")
    tx_obj = normalize(tx_data)
    parsed = parse(tx_obj)
    outcome = resolve(parsed)

    assert getattr(outcome, "who", None) is not None
    assert getattr(outcome, "minimum_amount_out", 0) > 0
    assert getattr(outcome, "type", None) == "buy"


def test_resolve_no_match():
    """
    Ensures that if no recognized instructions exist,
    we get an unknown/empty resolution.
    """
    from soltxs.parser.models import ParsedTransaction
    from soltxs.parser.parsers.unknown import Unknown as UnknownInstr
    from soltxs.resolver.resolvers.unknown import Unknown as UnknownResolve

    # A dummy set of instructions containing only Unknown.
    unknown_instructions = [
        UnknownInstr(
            program_id="FakeID",
            program_name="Unknown",
            instruction_name="Unknown",
            instruction_index=0,
        )
    ]
    # Build a dummy parsed_data dictionary.
    parsed_data = ParsedTransaction(**{"signatures": [], "instructions": unknown_instructions, "addons": {}})
    result = resolve(parsed_data)
    assert isinstance(result, UnknownResolve)
