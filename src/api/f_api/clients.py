from openai import OpenAI

from f_api.utils.azure_search import build_azure_search_store
from f_api.utils.embeddings import build_embeddings_model

openai = OpenAI()
embeddings = build_embeddings_model()
vector_store = build_azure_search_store(embeddings)
