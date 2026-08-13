"""
Builds one Ad Campaign record (Page URL + Custom label) for a single
property row. Field ordering in the custom label is FIXED per the
spec -- the consumer depends on positional order, so this must never
be reordered without a corresponding consumer-side change.

"""

from clients.config import AD_CAMPAIGN_PARTNER_NAME
from core.ads.percentile_lookup import get_property_score
from core.ads.price_segment import calculate_price_segment
from core.ads.tier_region_lookup import get_tier_region_info
from core.sitemap.sitemap_generator import url_for_property

VOID = "void"


def _fmt_number(value) -> str:
    """Strips a trailing .0 for whole numbers, keeps decimals otherwise. Returns VOID for None."""
    if value is None:
        return VOID
    try:
        f = float(value)
    except (TypeError, ValueError):
        return VOID
    if f.is_integer():
        return str(int(f))
    return str(f)


def build_page_url(row: dict) -> str:
    return url_for_property(row.get("external_id"), row.get("property_slug"))


def build_custom_label(row: dict) -> str:
    price_usd = row.get("price")
    segment = calculate_price_segment(price_usd)
    score = get_property_score(price_usd)
    tier_info = get_tier_region_info(row.get("country_code")) or {}

    fields = [
        "SINGLE_PRODUCT",
        row.get("city") or VOID,
        row.get("country") or VOID,
        row.get("property_type") or VOID,
        f"segments {segment}" if segment is not None else VOID,
        _fmt_number(price_usd),
        _fmt_number(score),
        VOID,  # position 8: void_field -- always literal "void" per spec
        AD_CAMPAIGN_PARTNER_NAME,
        tier_info.get("continent_code") or VOID,
        tier_info.get("tier_dest") or VOID,
        "property",  # position 12: literal constant per every example
        tier_info.get("region") or VOID,
    ]
    return ";".join(fields)


def build_ad_campaign_record(row: dict) -> dict:
    return {
        "Page URL": build_page_url(row),
        "Custom label": build_custom_label(row),
    }
