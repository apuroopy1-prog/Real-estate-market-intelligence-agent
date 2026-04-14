"""langsmith_eval.py — Evaluation suite for valuation accuracy"""
import json
from langsmith import Client
from langsmith.evaluation import evaluate

client = Client()

def correctness_evaluator(run, example):
    predicted = run.outputs.get("valuation_report", "")
    expected  = example.outputs.get("expected_recommendation", "")
    score = 1.0 if expected.lower() in predicted.lower() else 0.0
    return {"key": "recommendation_match", "score": score}

def run_eval(dataset_name: str = "real-estate-valuation-eval"):
    results = evaluate(
        lambda inputs: {"valuation_report": inputs.get("mock_output", "")},
        data=dataset_name,
        evaluators=[correctness_evaluator],
        experiment_prefix="real-estate-agent-eval",
    )
    print(results.to_pandas()[["input","output","recommendation_match"]].head())
