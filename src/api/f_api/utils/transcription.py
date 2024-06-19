from io import BytesIO
from typing import Any

from fastapi import UploadFile
from fastapi.responses import JSONResponse
from langchain_core.documents import Document
from openai import OpenAI
from openai.types.audio.transcription import Transcription

from f_api import config as cfg
from f_api.clients import embeddings, vector_store
from f_api.utils.diarization import diarize_audio
from f_api.utils.documents import insert_document_to_vectorstore


async def ingest_audio_impl(client: OpenAI, file: UploadFile) -> JSONResponse:
    try:
        if not file.filename:
            return JSONResponse(status_code=500, content={"detail": "Missing filename"})

        audio = await get_audio_buffer(file)
        transcription = get_transcription_from_bytes(client, audio)
        print(transcription)

        audio.seek(0)
        diarized = diarize_audio(
            audio_bytes=audio,
            transcription=transcription,
        )
        print(diarized)

        document = transcription_to_document(transcription, file.filename)
        insert_document_to_vectorstore(
            vector_store=vector_store,
            embeddings=embeddings,
            document=document,
        )

        return JSONResponse(
            status_code=200,
            content={
                "filename": file.filename,
                "transcription": diarized,
            },
        )
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"detail": str(e)})


async def get_audio_buffer(file: UploadFile) -> BytesIO:
    audio_bytes = await file.read()
    audio_buffer = BytesIO(audio_bytes)
    audio_buffer.name = file.filename
    return audio_buffer

def get_transcription_from_bytes(client: OpenAI, audio_file: BytesIO) -> Any:
    transcription = client.audio.transcriptions.create(
        model=cfg.TRANSCRIPTION_MODEL,
        file=audio_file,
        response_format="verbose_json",
        timestamp_granularities=["segment", "word"],
    )

    return transcription

def transcription_to_document(transcription: Transcription, filename: str) -> Document:
    return Document(
        page_content=transcription.text,
        metadata={
            "source": "audio_transcription",
            "filename": filename,
        }
    )
