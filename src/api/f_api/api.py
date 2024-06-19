from typing import Any

from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse
from langchain_core.documents import Document
from pydantic import BaseModel

from f_api.clients import embeddings, openai, vector_store
from f_api.utils.chat import chat_pipeline
from f_api.utils.documents import insert_document_to_vectorstore
from f_api.utils.transcription import ingest_audio_impl

app = FastAPI()

class DocumentRequest(BaseModel): # type: ignore
    content: str
    metadata: dict[str, Any]

class ChatRequest(BaseModel): # type: ignore
    prompt: str


@app.post("/audio") # type: ignore
async def ingest_audio(file: UploadFile) -> JSONResponse:
    return await ingest_audio_impl(
        client=openai,
        file=file,
    )


@app.post("/doc") # type: ignore
async def ingest_document(request: DocumentRequest) -> JSONResponse:
    document = Document(
        page_content=request.content,
        metadata=request.metadata,
    )
    insert_document_to_vectorstore(
        vector_store=vector_store,
        embeddings=embeddings,
        document=document,
    )

    return JSONResponse(status_code=200, content={"detail": "Success"})

@app.post("/chat") # type: ignore
async def chat(request: ChatRequest) -> JSONResponse:
    return chat_pipeline(
        vector_store=vector_store,
        prompt=request.prompt,
    )
