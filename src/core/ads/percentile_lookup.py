"""
Property score lookup: the smallest value in price_score_percentiles.json
that is >= the property's price, found via binary search (bisect) rather
than a linear scan, per the spec.
The percentile list is loaded from disk once and cached (lazy_singleton),
not re-read per property.
"""

import bisect
import json
from pathlib import Path

from clients.config import AD_CAMPAIGN_CONFIG_DIR, PRICE_PERCENTILES_FILENAME
from clients.lazy_singleton import lazy_singleton


def _load_percentiles() -> list[float]:
    path = Path(AD_CAMPAIGN_CONFIG_DIR) / PRICE_PERCENTILES_FILENAME
    if not path.exists():
        return []
    data = json.loads(path.read_text())
    return sorted(float(v) for v in data)


get_percentiles = lazy_singleton(_load_percentiles)


def get_property_score(price_usd) -> float | None:
    """
    Returns the smallest percentile value >= price_usd, or None if
    price is missing/invalid, or if no percentile value is >= price
    (price exceeds every percentile in the list) -- callers should
    render "void" for either case.
    """
    if price_usd is None:
        return None
    try:
        price = float(price_usd)
    except (TypeError, ValueError):
        return None

    percentiles = get_percentiles()
    if not percentiles:
        return None

    index = bisect.bisect_left(percentiles, price)
    if index >= len(percentiles):
        return None  # price exceeds every percentile value
    return percentiles[index]
