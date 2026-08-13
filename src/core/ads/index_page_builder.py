"""
Builds the feed index.html page listing every generated Ad Campaign CSV
file, matching the real-world format shown at
cdn.rentbyowner.com/v1/property-marketing-ads/property/property-all/index.html:
columns Campaign Type | Route | Feed Url | Location Names | Count | Status.

"Status" and "Location Names" are treated as fixed constants (matching
every row in the real reference page) rather than derived per-file --
these files aren't served over live HTTP in this project, so "202"
represents a fixed "generated/accepted" marker, not an actual response
code from a request.
"""

from html import escape

CAMPAIGN_TYPE = "page_feed"
ROUTE = "property"
LOCATION_NAMES = "all"
STATUS = "202"


def build_index_html(feed_entries: list[dict], base_url: str) -> str:
    """
    feed_entries: list of {"filename": ..., "count": ...} dicts, one per
    generated CSV file (already chunked/named by feed_partitioner.py).
    base_url: the URL prefix the CSV files are actually served from,
    used to build each clickable Feed Url link.
    """
    rows_html = []
    for entry in feed_entries:
        filename = entry["filename"]
        count = entry["count"]
        url = f"{base_url.rstrip('/')}/{filename}"
        rows_html.append(
            "  <tr>"
            f"<td>{escape(CAMPAIGN_TYPE)}</td>"
            f"<td>{escape(ROUTE)}</td>"
            f'<td><a href="{escape(url)}" download="{escape(filename)}">{escape(filename)}</a></td>'
            f"<td>{escape(LOCATION_NAMES)}</td>"
            f"<td>{count}</td>"
            f"<td>{escape(STATUS)}</td>"
            "</tr>"
        )

    return (
        "<!DOCTYPE html>\n"
        '<html>\n<head><meta charset="utf-8"><title>Ad Campaign Feeds</title></head>\n'
        "<body>\n"
        '<table border="1">\n'
        "  <tr><th>Campaign Type</th><th>Route</th><th>Feed Url</th>"
        "<th>Location Names</th><th>Count</th><th>Status</th></tr>\n" + "\n".join(rows_html) + "\n</table>\n</body>\n</html>\n"
    )
