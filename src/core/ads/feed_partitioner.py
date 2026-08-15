"""
Groups Ad Campaign records by continent, then splits each continent's
records into parts if the row count exceeds MAX_ROWS_PER_FILE (per the
consumer's file-size limit) -- producing the exact filename pattern
required: rbo_google_page_property_feed_booking_{continent}.csv for a
single file, or _{continent}_partN.csv when split.
"""

from core.ads.continent_slug import continent_slug

MAX_ROWS_PER_FILE = 70000
FILENAME_PREFIX = "rbo_google_page_property_feed_booking"


def group_by_continent(records_with_continent: list[tuple[dict, str | None]]) -> dict:
    """
    records_with_continent: list of (record, continent_code) pairs.
    Returns {continent_slug: [record, ...]}.
    """
    grouped: dict = {}
    for record, continent_code in records_with_continent:
        slug = continent_slug(continent_code)
        grouped.setdefault(slug, []).append(record)
    return grouped


def chunk_records(records: list[dict], chunk_size: int = MAX_ROWS_PER_FILE) -> list[list[dict]]:
    return [records[i : i + chunk_size] for i in range(0, len(records), chunk_size)]


def build_filenames_for_continent(slug: str, num_parts: int) -> list[str]:
    """
    1 part  -> rbo_google_page_property_feed_booking_{slug}.csv
    N parts -> rbo_google_page_property_feed_booking_{slug}_part1.csv, _part2.csv, ...
    """
    if num_parts == 1:
        return [f"{FILENAME_PREFIX}_{slug}.csv"]
    return [f"{FILENAME_PREFIX}_{slug}_part{i}.csv" for i in range(1, num_parts + 1)]
