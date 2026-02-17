
from fastapi import FastAPI
from app.api.routes import router, container
from app.ingestion.pipeline import IngestionPipeline
from app.vectorstore.faiss_store import FAISSVectorStore
from app.retrieval.retriever import SemanticRetriever
from app.llm.pipeline import RAGPipeline
from app.config import settings


app = FastAPI(title=settings.APP_NAME)


def initialize_app():

    # Ingestion
    ingestion = IngestionPipeline(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP
    )

    # Vector Store
    vector_store = FAISSVectorStore(
        embedding_model_name=settings.EMBEDDING_MODEL,
        persist_path=settings.VECTORSTORE_PATH
    )

    # Try loading existing index
    try:
        vector_store.load_index()
    except:
        pass

    # Retriever
    retriever = SemanticRetriever(
        vector_store=vector_store,
        top_k=settings.TOP_K,
        score_threshold=settings.SCORE_THRESHOLD
    )

    # RAG Pipeline
    rag_pipeline = RAGPipeline(
        retriever=retriever
    )

    # Inject into container
    container.ingestion = ingestion
    container.vector_store = vector_store
    container.retriever = retriever
    container.rag_pipeline = rag_pipeline


initialize_app()
app.include_router(router)

# app/main.py
