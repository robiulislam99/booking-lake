"""
Maps a continent_code (from tier_region_continent_map.json) to the
filename slug used in the CSV feed files (rbo_google_page_property_feed_
booking_{slug}.csv). Default behavior is continent_code.lower()
"""

CONTINENT_SLUG_OVERRIDES = {
    # "ASI": "as",   # example override if the real code doesn't match directly
}

UNMAPPED_SLUG = "unmapped"  # properties whose country has no continent mapping at all


def continent_slug(continent_code: str | None) -> str:
    if not continent_code:
        return UNMAPPED_SLUG
    return CONTINENT_SLUG_OVERRIDES.get(continent_code, continent_code.lower())
