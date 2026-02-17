from typing import List, Tuple
from langchain_core.documents import Document
from app.vectorstore.faiss_store import FAISSVectorStore
from app.config import settings

class SemanticRetriever:

    def __init__(
        self,
        vector_store: FAISSVectorStore,
        top_k: int = None,
        score_threshold: float = None
    ):
        self.vector_store = vector_store
        self.top_k = settings.TOP_K if top_k is None else top_k
        self.score_threshold = settings.SCORE_THRESHOLD if score_threshold is None else score_threshold
        

    def retrieve(self, query: str) -> List[Document]:

        if self.vector_store.index is None:
            raise ValueError("Vector index not initialized.")

        results: List[Tuple[Document, float]] = (
            self.vector_store.index.similarity_search_with_score(
                query,
                k=self.top_k
            )
        )

        filtered_docs = []

        for doc, score in results:
            print("Score:", score)
            print("Threshold:", self.score_threshold)
            
            # Fixed: This if statement is now INSIDE the loop
            if score <= self.score_threshold:
                filtered_docs.append(doc)

        print("Retrieved docs count:", len(filtered_docs))

        return filtered_docs

    def retrieve_with_scores(self, query: str) -> List[Tuple[Document, float]]:
        """
        Retrieve documents with their similarity scores.
        Used for evaluation purposes.
        """
        if self.vector_store.index is None:
            raise ValueError("Vector index not initialized.")

        results: List[Tuple[Document, float]] = (
            self.vector_store.index.similarity_search_with_score(
                query,
                k=self.top_k
            )
        )

        filtered_results = []

        for doc, score in results:
            if score <= self.score_threshold:
                filtered_results.append((doc, score))

        return filtered_results
    
# app/retrieval/retriever.py
