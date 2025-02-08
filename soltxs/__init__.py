from soltxs.normalizer import normalize
from soltxs.parser import parse
from soltxs.resolver import resolve

from soltxs import normalizer, parser, resolver


def process(tx: dict) -> resolver.models.Resolve:
    """
    Resolves a Solana transaction by normalizing, parsing, and then resolving it.

    Args:
        tx: The raw transaction payload as a dict.

    Returns:
        A resolved transaction object representing a human-readable interpretation.
    """
    normalized = normalize(tx)
    parsed = parse(normalized)
    resolved = resolve(parsed)

    return resolved
