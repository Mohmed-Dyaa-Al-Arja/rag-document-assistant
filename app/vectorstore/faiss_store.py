import os
from typing import List, Optional

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


class FAISSVectorStore:
    """
    Manages FAISS index lifecycle:
    - Create
    - Load
    - Save
    - Add documents
    - Provide retriever
    """

    def __init__(
        self,
        embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        persist_path: str = "data/vectorstore"
    ):
        self.persist_path = persist_path

        # Ensure persistence directory exists
        os.makedirs(self.persist_path, exist_ok=True)

        # Initialize embedding model
        self.embeddings = HuggingFaceEmbeddings(
            model_name=embedding_model_name
        )

        self.index: Optional[FAISS] = None

    # Index Creation

    def create_index(self, documents: List[Document]) -> None:
        """
        Create new FAISS index from documents.
        """
        self.index = FAISS.from_documents(
            documents=documents,
            embedding=self.embeddings
        )

    # Load Existing Index

    def load_index(self) -> None:
        """
        Load FAISS index from disk if exists.
        """
        if not os.path.exists(self.persist_path):
            raise FileNotFoundError("Vectorstore path does not exist.")

        self.index = FAISS.load_local(
            folder_path=self.persist_path,
            embeddings=self.embeddings,
            allow_dangerous_deserialization=True
        )

    # Save Index

    def save_index(self) -> None:
        """
        Persist FAISS index to disk.
        """
        if self.index is None:
            raise ValueError("No FAISS index to save.")

        self.index.save_local(self.persist_path)

    # Add Documents

    def add_documents(self, documents: List[Document]) -> None:
        """
        Add new documents to existing index.
        """
        if self.index is None:
            raise ValueError("Index not initialized.")

        self.index.add_documents(documents)

    # Get Retriever

    def as_retriever(self, k: int = 4):
        """
        Return retriever object for similarity search.
        """
        if self.index is None:
            raise ValueError("Index not initialized.")

        return self.index.as_retriever(
            search_kwargs={"k": k}
        )
    
    
# app/vectorstore/faiss_store.py
