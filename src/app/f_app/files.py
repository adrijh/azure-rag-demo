import requests
from streamlit.runtime.uploaded_file_manager import UploadedFile

from f_app.config import AUDIO_ENDPOINT, DOC_ENDPOINT
from f_app.documents import transform_files_to_documents


def process_text_files(text_files: list[UploadedFile]) -> list[requests.Response]:
    text_documents = transform_files_to_documents(text_files)

    responses = []
    for text_doc in text_documents:
        response = requests.post(
            url=DOC_ENDPOINT,
            json={
                "content": text_doc.page_content,
                "metadata": text_doc.metadata,
            },
            timeout=30,
        )
        responses.append(response)

    return responses

def process_audio_files(audio_files: list[UploadedFile]) -> list[requests.Response]:
    responses = []
    for audio_file in audio_files:
        print("Sending request")
        response = requests.post(
            url=AUDIO_ENDPOINT,
            files={"file": (audio_file.name, audio_file, audio_file.type)},
            timeout=300,
        )
        print(response)
        responses.append(response)

    return responses
