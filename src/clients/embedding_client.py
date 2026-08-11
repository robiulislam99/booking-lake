"""
Lazy-loaded sentence-transformers embedding model, used to turn a
property's text description into a 384-dim vector for Qdrant similarity
search. Loaded once per process and reused -- loading it per-call would
be very slow.
"""

import os

from sentence_transformers import SentenceTransformer

from . import config as client_config

MODEL_NAME = client_config.EMBEDDING_MODEL_NAME
_model = None


def _get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(os.environ.get("EMBEDDING_MODEL_NAME", MODEL_NAME))
    return _model


def generate_embedding(text: str) -> list[float]:
    """Turns one piece of text into a 384-dim embedding vector."""
    model = _get_model()
    vector = model.encode(text, convert_to_numpy=True)
    return vector.tolist()
