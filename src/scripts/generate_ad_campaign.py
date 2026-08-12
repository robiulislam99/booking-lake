"""
Generates the Ad Campaign export: one CSV file per continent (split
into _part1/_part2/... if a continent exceeds MAX_ROWS_PER_FILE rows),
each with a "Page URL","Custom label" header row, written to the
project's local S3-compatible storage.

Usage: python generate_ad_campaign.py [YYYYMMDD]
(date arg only affects the output partition path -- this reads the
CURRENT full set of published properties, same "no changelog
filtering" tradeoff as export_to_s3_local.py's original design.)
"""

import sys
from datetime import datetime

from clients.s3_local_client import LocalS3Client
from clients.spark_session import get_spark
from core.ads.csv_writer import render_ad_campaign_csv
from core.ads.custom_label_builder import build_ad_campaign_record
from core.ads.feed_partitioner import build_filenames_for_continent, chunk_records, group_by_continent
from core.ads.tier_region_lookup import get_tier_region_info

TABLE = "local.booking.rental_property"
BUCKET_NAME = "booking-lake-bucket"


def load_published_rows_iterator(spark):
    df = spark.sql(f"""
        SELECT external_id, property_slug, city, country, country_code,
               property_type, price, is_published
        FROM {TABLE}
        WHERE is_published = true
    """)
    return (row.asDict() for row in df.toLocalIterator())


def main():
    date_str = sys.argv[1] if len(sys.argv) > 1 else datetime.utcnow().strftime("%Y%m%d")

    spark = get_spark("generate-ad-campaign")
    try:
        rows = load_published_rows_iterator(spark)

        records_with_continent = []
        for row in rows:
            record = build_ad_campaign_record(row)
            tier_info = get_tier_region_info(row.get("country_code")) or {}
            records_with_continent.append((record, tier_info.get("continent_code")))

        if not records_with_continent:
            print("No published properties found -- nothing to generate.")
            return

        grouped = group_by_continent(records_with_continent)

        client = LocalS3Client()
        client.create_bucket(Bucket=BUCKET_NAME)

        total_files = 0
        total_rows = 0
        for slug, records in grouped.items():
            chunks = chunk_records(records)
            filenames = build_filenames_for_continent(slug, len(chunks))

            for filename, chunk in zip(filenames, chunks, strict=False):
                csv_content = render_ad_campaign_csv(chunk)
                key = f"ad-campaigns/date={date_str}/{filename}"
                client.put_object(Bucket=BUCKET_NAME, Key=key, Body=csv_content.encode("utf-8"))
                print(f"Wrote {len(chunk)} row(s) to s3://{BUCKET_NAME}/{key}")
                total_files += 1
                total_rows += len(chunk)

        print(f"\nDone: {total_rows} row(s) across {total_files} file(s), " f"{len(grouped)} continent group(s)")

    finally:
        spark.stop()


if __name__ == "__main__":
    main()
