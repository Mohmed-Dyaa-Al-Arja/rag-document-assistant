import os
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import StreamingResponse
from shutil import copyfileobj

from app.schemas.models import (
    QuestionRequest,
    QuestionResponse,
    UploadResponse
)
from app.ingestion.pipeline import IngestionPipeline
from app.vectorstore.faiss_store import FAISSVectorStore
from app.retrieval.retriever import SemanticRetriever
from app.llm.pipeline import RAGPipeline
from app.security.auth import verify_api_key


router = APIRouter()


class AppContainer:
    ingestion: IngestionPipeline = None
    vector_store: FAISSVectorStore = None
    retriever: SemanticRetriever = None
    rag_pipeline: RAGPipeline = None
    sessions = {}


container = AppContainer()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/upload", response_model=UploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    api_key: str = Depends(verify_api_key)
):

    try:
        save_path = f"data/documents/{file.filename}"
        os.makedirs("data/documents", exist_ok=True)

        with open(save_path, "wb") as buffer:
            copyfileobj(file.file, buffer)

        chunks = container.ingestion.ingest(save_path)

        if container.vector_store.index is None:
            container.vector_store.create_index(chunks)
        else:
            container.vector_store.add_documents(chunks)

        container.vector_store.save_index()

        return UploadResponse(
            message="Document processed successfully.",
            total_chunks=len(chunks)
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ask", response_model=QuestionResponse)
async def ask_question(
    request: QuestionRequest,
    api_key: str = Depends(verify_api_key)
):

    if container.retriever is None:
        raise HTTPException(status_code=400, detail="System not initialized.")

    session_id = request.session_id

    if session_id not in container.sessions:
        container.sessions[session_id] = RAGPipeline(container.retriever)

    pipeline = container.sessions[session_id]

    result = await pipeline.ask_async(request.question)

    return QuestionResponse(**result)


@router.post("/ask-stream")
async def ask_stream(
    request: QuestionRequest,
    api_key: str = Depends(verify_api_key)
):

    session_id = request.session_id

    if session_id not in container.sessions:
        container.sessions[session_id] = RAGPipeline(container.retriever)

    pipeline = container.sessions[session_id]

    async def token_generator():
        async for token in pipeline.ask_stream(request.question):
            yield token

    return StreamingResponse(
        token_generator(),
        media_type="text/plain"
    )


@router.post("/clear-memory")
async def clear_memory(
    request: QuestionRequest,
    api_key: str = Depends(verify_api_key)
):

    session_id = request.session_id

    if session_id in container.sessions:
        container.sessions[session_id].memory.clear()

    return {"message": "Conversation memory cleared."}

# app/api/routes.py
