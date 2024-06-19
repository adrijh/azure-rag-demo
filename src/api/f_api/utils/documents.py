from typing import Any

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore
from langchain_experimental.text_splitter import SemanticChunker


def chunk_documents(documents: list[Document], embeddings: Embeddings) -> Any:
    text_splitter = SemanticChunker(embeddings)
    return text_splitter.split_documents(documents)


def insert_document_to_vectorstore(
    vector_store: VectorStore,
    embeddings: Embeddings,
    document: Document,
) -> None:
    document_chunks = chunk_documents(
        documents=[document],
        embeddings=embeddings,
    )
    vector_store.add_documents(document_chunks)
