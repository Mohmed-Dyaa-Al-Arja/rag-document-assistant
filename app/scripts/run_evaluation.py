from app.evaluation.evaluator import RetrievalEvaluator
from app.api.routes import container

questions = [
    "What is the termination clause?",
    "What is the payment schedule?",
    "What are the penalties?"
]

evaluator = RetrievalEvaluator(container.retriever)
metrics = evaluator.evaluate(questions)

print(metrics)

# app/scripts/run_evaluation.py
