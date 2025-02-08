from typing import Any, Dict

from soltxs import parser
from soltxs.resolver import models, resolvers


def resolve(parsed_data: Dict[str, Any]) -> models.Resolve:
    """
    Translates the parsed transaction data into a final human-readable interpretation.

    Args:
        parsed_data: A dictionary with parsed transaction details.

    Returns:
        A resolved transaction object.
    """
    instructions = parsed_data.get("instructions", [])
    for transformer in (resolvers.pumpfun.PumpFunResolver, resolvers.raydium.RaydiumResolver):
        result = transformer.resolve(instructions)
        if result is not None:
            return result

    return resolvers.unknown.UnknownResolver.resolve(instructions)
