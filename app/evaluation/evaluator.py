from typing import List, Dict
from statistics import mean
from app.retrieval.retriever import SemanticRetriever


class RetrievalEvaluator:
    """
    Evaluates retrieval performance of the RAG system.
    Focuses on:
    - Hit Rate
    - Average Similarity Score
    - Empty Retrieval Rate
    """

    def __init__(self, retriever: SemanticRetriever):
        self.retriever = retriever

    def evaluate(self, questions: List[str]) -> Dict[str, float]:
        """
        Run evaluation on a list of questions.
        """

        total_questions = len(questions)
        if total_questions == 0:
            raise ValueError("No questions provided for evaluation.")

        hit_count = 0
        empty_count = 0
        similarity_scores = []

        for question in questions:

            # Retrieve with scores
            results = self.retriever.retrieve_with_scores(question)

            if not results:
                empty_count += 1
                continue

            hit_count += 1

            # Collect similarity scores
            for _, score in results:
                similarity_scores.append(score)

        hit_rate = hit_count / total_questions
        empty_rate = empty_count / total_questions
        avg_score = mean(similarity_scores) if similarity_scores else 0.0

        return {
            "total_questions": total_questions,
            "hit_rate": round(hit_rate, 3),
            "empty_retrieval_rate": round(empty_rate, 3),
            "average_similarity_score": round(avg_score, 3),
        }
# app/evaluation/evaluator.py
