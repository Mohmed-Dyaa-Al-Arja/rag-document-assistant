from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # Application
    APP_NAME: str = "RAG Document Assistant"
    ENVIRONMENT: str = "development"

    # Security
    RAG_API_KEY: str = "dev-secret-key"

    # Vector Store
    VECTORSTORE_PATH: str = "data/vectorstore"
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    # Ingestion
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200

    # Retrieval
    TOP_K: int = 4
    SCORE_THRESHOLD: float = 3.0

    # LLM Provider Mode
    LLM_PROVIDER: str = "auto"   # auto | gemini | ollama

    # Gemini
    GEMINI_API_KEY: str | None = None
    GEMINI_MODEL: str = "gemini-2.5-flash"

    # Ollama
    OLLAMA_MODEL: str = "llama3.1:8b"
    OLLAMA_BASE_URL: str = "http://localhost:11434"

    # File Upload
    MAX_FILE_SIZE_MB: int = 10
    ALLOWED_EXTENSIONS: list[str] = [".pdf", ".docx"]

    class Config:
        env_file = ".env"


settings = Settings()

# app/config.py
