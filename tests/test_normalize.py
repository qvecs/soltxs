import pytest
from soltxs import normalize
from soltxs.normalizer.models import Transaction


def test_rpc_transaction():
    """
    Test that an RPC-style transaction JSON is parsed (normalized) correctly.
    """
    data = {
        "jsonrpc": "2.0",
        "result": {
            "slot": 123456,
            "blockTime": 1678900000,
            "transaction": {
                "signatures": ["someSignature"],
                "message": {
                    "accountKeys": [
                        "111111111111111111111111111111111",  # 33 ones => unify
                        "ExamplePubkey2",
                    ],
                    "recentBlockhash": "SomeBlockhashValue",
                    "instructions": [
                        {
                            "programIdIndex": 0,
                            "data": "abc123",
                            "accounts": [1, 2],
                        }
                    ],
                },
            },
            "meta": {
                "fee": 5000,
                "preBalances": [1000, 2000],
                "postBalances": [900, 2100],
                "preTokenBalances": [],
                "postTokenBalances": [],
                "innerInstructions": [],
                "logMessages": ["Program log: example"],
                "err": None,
                "status": {"Ok": None},
                "computeUnitsConsumed": 12345,
            },
        },
    }

    tx = normalize(data)
    assert isinstance(tx, Transaction)
    assert tx.slot == 123456
    assert tx.blockTime == 1678900000
    assert tx.message.accountKeys[0] == "11111111111111111111111111111111"  # unified
    assert tx.meta.fee == 5000
    assert tx.meta.computeUnitsConsumed == 12345
    assert tx.meta.logMessages == ["Program log: example"]


def test_geyser_transaction():
    """
    Test that a Geyser-style transaction JSON is parsed (normalized) correctly.
    """
    data = {
        "transaction": {
            "slot": 654321,
            "transaction": {
                "meta": {
                    "fee": 6000,
                    "preBalances": [3000, 4000],
                    "postBalances": [2500, 4500],
                    "preTokenBalances": [],
                    "postTokenBalances": [],
                    "innerInstructions": [],
                    "logMessages": ["Program log: geyser example"],
                    "err": None,
                    "status": {"Ok": None},
                    "computeUnitsConsumed": 23456,
                    "loadedWritableAddresses": ["SomeWritableAddr"],
                    "loadedReadonlyAddresses": ["SomeReadonlyAddr"],
                },
                "transaction": {
                    "signatures": ["geyserSignature"],
                    "message": {
                        "accountKeys": [
                            "111111111111111111111111111111111",  # 33 ones => unify
                            "GeyserPubkey2",
                        ],
                        "recentBlockhash": "GeyserBlockhashValue",
                        "instructions": [
                            {
                                "programIdIndex": 1,
                                "data": "def456",
                                "accounts": [0],
                            }
                        ],
                        "addressTableLookups": [],
                    },
                },
            },
        }
    }

    tx = normalize(data)
    assert isinstance(tx, Transaction)
    assert tx.slot == 654321
    assert tx.blockTime is None  # Geyser has no block_time
    assert tx.message.accountKeys[0] == "11111111111111111111111111111111"
    assert tx.meta.fee == 6000
    assert tx.meta.computeUnitsConsumed == 23456
    assert tx.loadedAddresses.writable == ["SomeWritableAddr"]
    assert tx.loadedAddresses.readonly == ["SomeReadonlyAddr"]


def test_unrecognized_transaction():
    """
    Test that an unrecognized transaction format raises ValueError.
    """
    data = {"invalid": "format"}

    with pytest.raises(ValueError):
        normalize(data)


def test_equal_transaction(load_data):
    """
    Test that two transactions with the same data are equal after normalization.
    """
    tx1 = normalize(load_data("raydium_amm_v4_geyser.json"))
    tx2 = normalize(load_data("raydium_amm_v4_rpc.json"))

    # Geyser block_time is None; unify for comparison.
    tx1.blockTime = None
    tx2.blockTime = None

    assert tx1 == tx2
