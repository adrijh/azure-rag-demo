from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore

from f_api import config as cfg


def build_azure_search_store(embeddings: Embeddings) -> VectorStore:
    return AzureSearch(
        azure_search_endpoint=cfg.AZURE_SEARCH_ENDPOINT,
        azure_search_key=cfg.AZURE_SEARCH_KEY,
        index_name=cfg.AZURE_SEARCH_INDEX_NAME,
        embedding_function=embeddings.embed_query,
    )
