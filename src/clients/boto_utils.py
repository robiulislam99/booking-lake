"""
Shared boto3 client/resource construction for local AWS-emulator
services (SQS via LocalStack, DynamoDB via DynamoDB Local). Both need
the same shape of setup: a fake test credential pair, a region, and a
local endpoint_url override -- this was previously duplicated between
sqs_client.py and dynamodb_client.py.
"""

import boto3

from .config import AWS_ACCESS_KEY_ID, AWS_REGION, AWS_SECRET_ACCESS_KEY


def _boto3_kwargs(endpoint_url: str | None) -> dict:
    kwargs = {
        "region_name": AWS_REGION,
        "aws_access_key_id": AWS_ACCESS_KEY_ID,
        "aws_secret_access_key": AWS_SECRET_ACCESS_KEY,
    }
    if endpoint_url:
        kwargs["endpoint_url"] = endpoint_url
    return kwargs


def get_boto3_client(service_name: str, endpoint_url: str):
    return boto3.client(service_name, **_boto3_kwargs(endpoint_url))


def get_boto3_resource(service_name: str, endpoint_url: str):
    return boto3.resource(service_name, **_boto3_kwargs(endpoint_url))
