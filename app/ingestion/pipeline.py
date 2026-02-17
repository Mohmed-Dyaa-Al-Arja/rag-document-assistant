from typing import List
from langchain_core.documents import Document
from app.ingestion.loader import DocumentLoader
from app.ingestion.splitter import DocumentSplitter


class IngestionPipeline:
    """
    Full ingestion pipeline:
    Load → Split → Return chunks
    """

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ):
        self.loader = DocumentLoader()
        self.splitter = DocumentSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    def ingest(self, file_path: str) -> List[Document]:
        """
        Execute ingestion pipeline.
        """
        # Step 1: Load raw document
        documents = self.loader.load(file_path)

        # Step 2: Split into chunks
        chunks = self.splitter.split(documents)

        return chunks
# app/ingestion/pipeline.py
