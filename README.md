# Multi Modal RAG in Azure

In previous demo repository we explored the architecture of a basic RAG system, reduced to its core components.
In this article we will show additional techniques we can use to improve the performance of our application like Semantic Chunking, Query Expansion and Reranking.
We also added support for audio transcription and diarization.

In addition, we will move towards a more decoupled architecture. We will separate our Streamlit interface from our RAG System. For that purpose, we develop a simple FastAPI application to serve as backend.
