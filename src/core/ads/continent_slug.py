"""
Maps a continent code to the filename suffix used in the CSV feed files.
If a property has no continent mapping, use "unmapped".
"""

UNMAPPED_SLUG = "unmapped"


def continent_slug(continent_code: str | None) -> str:
    if not continent_code:
        return UNMAPPED_SLUG

    return continent_code.lower()
