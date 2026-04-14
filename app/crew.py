"""crew.py — Crew orchestration with cost tracking"""
import os
from crewai import Crew, Process
from langsmith_config import setup_langsmith
from app.agents import build_agents
from app.tasks import build_tasks
from utils.cost_tracker import TokenBudget, BudgetExceededError

setup_langsmith("project-01-real-estate-intelligence")


def run_valuation_crew(property_data: dict) -> dict:
    """Run the 3-agent real estate valuation crew."""
    budget = TokenBudget(
        max_tokens=int(os.getenv("TOKEN_BUDGET", 80_000)),
        model="gpt-4o"
    )

    comps_analyst, trend_analyst, report_writer = build_agents()
    task1, task2, task3 = build_tasks(comps_analyst, trend_analyst, report_writer, property_data)

    crew = Crew(
        agents=[comps_analyst, trend_analyst, report_writer],
        tasks=[task1, task2, task3],
        process=Process.sequential,
        verbose=True,
    )

    try:
        with budget:
            result = crew.kickoff()
    except BudgetExceededError as e:
        return {"error": str(e), "partial_result": str(result)}

    return {
        "valuation_report": str(result),
        "token_summary": budget.summary(),
        "estimated_cost": budget.estimated_cost(),
    }
