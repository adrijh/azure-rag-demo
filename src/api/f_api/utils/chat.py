from fastapi.responses import JSONResponse
from langchain_core.vectorstores import VectorStore

from f_api.utils.embeddings import build_rag_chain


def chat_pipeline(
    vector_store: VectorStore,
    prompt: str,
) -> JSONResponse:
    rag_chain = build_rag_chain(vector_store)
    response = rag_chain.invoke(prompt)
    return JSONResponse(status_code=200, content={"message": response})
