from chromadb import HttpClient
from django.conf import settings

from .date_filter import get_date_filter
from .google_generative_ai import get_embeddings
from httpcore import ConnectError
from core.exceptions import VectorDbUnavailableException
import logging

logger = logging.getLogger(__name__)

COLLECTION_NAME = settings.CHROMADB_COLLECTION_NAME
CHROMADB_HOST = settings.CHROMADB_HOST
CHROMADB_PORT = settings.CHROMADB_PORT


def get_client():
    try:
        return HttpClient(host=CHROMADB_HOST, port=CHROMADB_PORT)
    except ConnectError as e:
        logger.error("Connection to ChromaDB failed: %s", e)
        raise VectorDbUnavailableException("Connection Refused by chroma") from e
    except Exception as e:
        logger.error("Unexpected error occurred: %s", e)
        raise Exception from e


def embed_text(texts, event_id, event_date):
    collection = get_client().get_or_create_collection(COLLECTION_NAME)
    timestamp = event_date.timestamp()

    collection.add(
        documents=texts,
        embeddings=get_embeddings(texts),
        metadatas=[{"event_ts": int(timestamp)}],
        ids=[str(event_id)],
    )


def query_text(query):
    client = get_client()
    collection = client.get_collection(COLLECTION_NAME)

    date_filter = get_date_filter(query)
    logger.debug("Date filter for query '%s': %s", query, date_filter)
    return collection.query(
        query_embeddings=get_embeddings(query), n_results=6, where=date_filter
    )
