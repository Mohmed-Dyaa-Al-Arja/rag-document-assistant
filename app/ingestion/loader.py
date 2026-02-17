from pathlib import Path
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import PyMuPDFLoader, Docx2txtLoader



class DocumentLoader:
    """
    Handles loading and parsing of supported document types.
    """

    SUPPORTED_EXTENSIONS = [".pdf", ".docx"]

    def load(self, file_path: str) -> List[Document]:
        """
        Load document and return list of LangChain Documents.
        """
        path = Path(file_path)

        if path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(f"Unsupported file type: {path.suffix}")

        if path.suffix.lower() == ".pdf":
            loader = PyMuPDFLoader(file_path)
        else:
            loader = Docx2txtLoader(file_path)

        documents = loader.load()

        return documents
# app/ingestion/loader.py
