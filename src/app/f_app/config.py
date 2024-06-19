import os

ENDPOINT_URL = os.getenv("ENDPOINT_URL", "http://localhost:8000")
DOC_ENDPOINT = f"{ENDPOINT_URL}/doc"
AUDIO_ENDPOINT = f"{ENDPOINT_URL}/audio"
CHAT_ENDPOINT = f"{ENDPOINT_URL}/chat"
