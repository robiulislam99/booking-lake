"""
Tier/region/continent lookup by country code, from
tier_region_continent_map.json. Loaded once and cached (lazy_singleton),
not re-read per property.
"""

import json
from pathlib import Path

from clients.config import AD_CAMPAIGN_CONFIG_DIR, TIER_REGION_MAP_FILENAME
from clients.lazy_singleton import lazy_singleton


def _load_tier_region_map() -> dict:
    path = Path(AD_CAMPAIGN_CONFIG_DIR) / TIER_REGION_MAP_FILENAME
    if not path.exists():
        return {}
    return json.loads(path.read_text())


get_tier_region_map = lazy_singleton(_load_tier_region_map)


def get_tier_region_info(country_code: str) -> dict | None:
    """
    Returns {"continent_code", "region_code", "tier_dest"} for a country
    code, or None if the country isn't in the map -- callers should
    render "void" for each missing field individually, not fail the
    whole record.
    """
    if not country_code:
        return None
    tier_map = get_tier_region_map()
    return tier_map.get(country_code.upper()) or tier_map.get(country_code.lower())
