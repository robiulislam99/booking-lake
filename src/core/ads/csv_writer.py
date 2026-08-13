"""
Renders Ad Campaign records (Page URL + Custom label) as CSV text.

"""

import csv
import io

CSV_HEADER = ["Page URL", "Custom label"]


def render_ad_campaign_csv(records: list[dict]) -> str:
    """records: list of {"Page URL": ..., "Custom label": ...} dicts."""
    buffer = io.StringIO()
    writer = csv.writer(buffer, quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
    writer.writerow(CSV_HEADER)
    for record in records:
        writer.writerow([record["Page URL"], record["Custom label"]])
    return buffer.getvalue()
