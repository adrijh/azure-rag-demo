from langchain_core.documents import Document
from streamlit.runtime.uploaded_file_manager import UploadedFile


def log_document(doc: str) -> str:
    print(doc)
    return doc

def transform_files_to_documents(
    uploaded_files: list[UploadedFile],
) -> list[Document]:
    documents = []
    for uploaded_file in uploaded_files:
        content = uploaded_file.read().decode("utf-8")
        doc = Document(page_content=content, metadata={"filename": uploaded_file.name})
        documents.append(doc)

    return documents
