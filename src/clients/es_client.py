from elasticsearch import Elasticsearch, helpers

from .config import ELASTICSEARCH_URL, ES_INDEX_NAME

ES_URL = ELASTICSEARCH_URL
INDEX_NAME = ES_INDEX_NAME

INDEX_MAPPING = {
    "mappings": {
        "properties": {
            "lonlat": {"type": "geo_point"},
        }
    }
}


def get_es_client() -> Elasticsearch:
    return Elasticsearch(ELASTICSEARCH_URL)


def ensure_index(es: Elasticsearch):
    if not es.indices.exists(index=ES_INDEX_NAME):
        es.indices.create(index=ES_INDEX_NAME, body=INDEX_MAPPING)


def bulk_upsert(es: Elasticsearch, documents: list):
    """documents: list of dicts, each must have an 'id' key used as _id."""
    ensure_index(es)
    actions = [{"_op_type": "index", "_index": ES_INDEX_NAME, "_id": doc["id"], "_source": doc} for doc in documents]
    helpers.bulk(es, actions)
