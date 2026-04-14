"""agents.py — CrewAI agent definitions for Real Estate Market Intelligence"""
import os
from crewai import Agent
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o", temperature=0.1, api_key=os.getenv("OPENAI_API_KEY"))


def build_agents():
    comps_analyst = Agent(
        role="Comparable Sales Analyst",
        goal="Find and score the 5 most relevant comparable property sales for the target property",
        backstory=(
            "You are a certified real estate appraiser with 12 years of experience in "
            "residential and commercial property valuation. You identify the best comparable "
            "sales (comps) by matching property type, size, age, condition, and location "
            "proximity. You score each comp on a 0-100 similarity scale."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=3,
    )

    trend_analyst = Agent(
        role="Market Trend Analyst",
        goal="Analyse 90-day price trends, days-on-market, and supply/demand signals for the target area",
        backstory=(
            "You are a real estate market economist specialising in hyperlocal market analysis. "
            "You track median price per sqft, days-on-market trends, list-to-sale price ratios, "
            "and absorption rates to determine whether a market is appreciating, stable, or declining."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=3,
    )

    report_writer = Agent(
        role="Valuation Report Writer",
        goal="Produce a structured investor-grade property valuation report with a buy/sell/hold recommendation",
        backstory=(
            "You are a senior real estate investment analyst who writes clear, data-backed "
            "valuation reports for institutional investors and property funds. Your reports "
            "include estimated market value, confidence band, cap rate estimate, and an "
            "explicit buy/sell/hold recommendation with supporting rationale."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=3,
    )

    return comps_analyst, trend_analyst, report_writer
