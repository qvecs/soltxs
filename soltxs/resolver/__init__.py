from soltxs.parser.models import ParsedTransaction
from soltxs.resolver import models, resolvers


def resolve(parsed_tx: ParsedTransaction) -> models.Resolve:
    """
    Translates the parsed transaction data into a final human-readable interpretation.

    Args:
        parsed_data: A dictionary with parsed transaction details.

    Returns:
        A resolved transaction object.
    """
    for transformer in (resolvers.pumpfun.PumpFunResolver, resolvers.raydium.RaydiumResolver):
        result = transformer.resolve(parsed_tx.instructions)
        if result is not None:
            return result

    return resolvers.unknown.UnknownResolver.resolve(parsed_tx.instructions)
