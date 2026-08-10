from . import client as _client

# Re-export the well-known client aliases from the registry module.
dynamodb = _client.dynamodb
es = _client.es
embedding = _client.embedding
qdrant = _client.qdrant
s3_local = _client.s3_local
spark = _client.spark
sqs = _client.sqs

__all__ = ["dynamodb", "es", "embedding", "qdrant", "s3_local", "spark", "sqs"]
