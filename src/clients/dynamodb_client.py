"""
Thin boto3 wrapper pointed at DynamoDB Local instead of real AWS --
same official image AWS themselves publish for local dev/testing, no
AWS account or credentials needed, just a local endpoint_url.

Table design: partition key property_id, sort key timestamp -- this
lets you store one item per (property, sync date) pair, so you can see
a property's history over time rather than only its latest state,
which is a common real-world DynamoDB access pattern worth practicing.
"""

import boto3

from .boto_utils import get_boto3_resource
from .config import DYNAMODB_ENDPOINT_URL, DYNAMODB_TABLE_NAME

TABLE_NAME = DYNAMODB_TABLE_NAME


def _resource():
    return get_boto3_resource("dynamodb", DYNAMODB_ENDPOINT_URL)


def ensure_table():
    dynamodb = _resource()
    existing = [t.name for t in dynamodb.tables.all()]
    if DYNAMODB_TABLE_NAME in existing:
        return dynamodb.Table(DYNAMODB_TABLE_NAME)

    table = dynamodb.create_table(
        TableName=DYNAMODB_TABLE_NAME,
        KeySchema=[
            {"AttributeName": "property_id", "KeyType": "HASH"},
            {"AttributeName": "timestamp", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "property_id", "AttributeType": "S"},
            {"AttributeName": "timestamp", "AttributeType": "S"},
        ],
        BillingMode="PAY_PER_REQUEST",
    )
    table.wait_until_exists()
    return table


def get_table():
    return _resource().Table(DYNAMODB_TABLE_NAME)


def batch_put_items(items: list):
    table = ensure_table()
    with table.batch_writer(overwrite_by_pkeys=["property_id", "timestamp"]) as batch:
        for item in items:
            batch.put_item(Item=item)


def get_item(property_id: str, timestamp: str):
    table = get_table()
    response = table.get_item(Key={"property_id": property_id, "timestamp": timestamp})
    return response.get("Item")


def query_by_property(property_id: str):
    """All timestamped snapshots for one property, e.g. its history over time."""
    table = get_table()
    response = table.query(KeyConditionExpression=boto3.dynamodb.conditions.Key("property_id").eq(property_id))
    return response.get("Items", [])
