import streamlit as st
from requests import Response
from streamlit.runtime.uploaded_file_manager import UploadedFile

from f_app.files import process_audio_files, process_text_files


class KnowledgeBasePage:
    def __init__(self) -> None:
        # st.header("RAG Parameters")
        # self.chunk_size = st.slider("Chunk Size", min_value=500, max_value=2000, value=1000)
        # self.chunk_overlap = st.slider("Chunk Overlap", min_value=0, max_value=100, value=25)

        st.header("Upload Files")

        upload_files = st.file_uploader(
            label="text_file_uploader",
            type=("txt", "md", "mp3", "wav"),
            accept_multiple_files=True,
            label_visibility="collapsed",
        )

        if st.button("Load", type="primary", use_container_width=True):
            result = ""
            if not upload_files:
                st.error("No files were included for upload.")
            else:
                result = self.__load_button_impl(upload_files)

            st.text_area(
                label="Retrieved document",
                value=result,
                height=640,
                key="transcription",
            )

    def __load_button_impl(self, upload_files: list[UploadedFile]) -> str:
        print(upload_files)
        text_files = filter(
            lambda file: file.type == "application/octet-stream",
            upload_files,
        )
        print(text_files)

        audio_files = filter(
            lambda file: file.type == "audio/mpeg",
            upload_files,
        )

        process_text_files(list(text_files))
        audio_responses = process_audio_files(list(audio_files))

        return self.__format_responses(audio_responses)

    def __format_responses(self, responses: list[Response]) -> str:
        text_response = ""
        for response in responses:
            response_dict = response.json()
            filename = response_dict.get("filename")
            transcription = response_dict.get("transcription")

            if not filename or not transcription:
                continue

            text_response += f"{filename}\n"
            text_response += f"{transcription}\n"

        return text_response


if __name__ == "__main__":
    KnowledgeBasePage()
