"""
Centralized environment-variable configuration for every client. Single
source of truth for defaults -- avoids the same setting (e.g. AWS
region, table/index names) being read with slightly different defaults
in two different files.
"""

import os

# --- AWS-style local emulators (SQS, DynamoDB) ---
AWS_REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "test")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "test")

SQS_ENDPOINT_URL = os.environ.get("SQS_ENDPOINT_URL", "http://localstack:4566")
SQS_QUEUE_NAME = os.environ.get("SQS_QUEUE_NAME", "booking-property-updates")

DYNAMODB_ENDPOINT_URL = os.environ.get("DYNAMODB_ENDPOINT_URL", "http://dynamodb-local:8000")
DYNAMODB_TABLE_NAME = os.environ.get("DYNAMODB_TABLE_NAME", "rental_properties")

# --- Elasticsearch ---
ELASTICSEARCH_URL = os.environ.get("ELASTICSEARCH_URL", "http://elasticsearch:9200")
ES_INDEX_NAME = os.environ.get("ES_INDEX_NAME", "rental_properties")

# --- Qdrant ---
QDRANT_URL = os.environ.get("QDRANT_URL", "http://qdrant:6333")
QDRANT_COLLECTION_NAME = os.environ.get("QDRANT_COLLECTION_NAME", "rental_properties")
QDRANT_VECTOR_SIZE = int(os.environ.get("QDRANT_VECTOR_SIZE", "384"))

# --- S3-local ---
S3_LOCAL_ROOT = os.environ.get("S3_LOCAL_ROOT", "/app/s3_local")

# --- Embedding model ---
EMBEDDING_MODEL_NAME = os.environ.get("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")

# --- Ad Campaign feature ---
AD_CAMPAIGN_CONFIG_DIR = os.environ.get("AD_CAMPAIGN_CONFIG_DIR", "/app/booking_data")
AD_CAMPAIGN_PARTNER_NAME = os.environ.get("AD_CAMPAIGN_PARTNER_NAME", "BOOKING.COM")
PRICE_PERCENTILES_FILENAME = "price_score_percentiles.json"
TIER_REGION_MAP_FILENAME = "tier_region_continent_map.json"


AD_CAMPAIGN_FEED_BASE_URL = os.environ.get(
    "AD_CAMPAIGN_FEED_BASE_URL",
    "https://cdn.rentbyowner.com/v1/property-marketing-ads/property/property-all/example",
)
