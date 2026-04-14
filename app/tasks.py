"""tasks.py — Task definitions with Instructor-validated outputs"""
import instructor
import openai
from crewai import Task
from pydantic import BaseModel, Field
from typing import Literal, Optional

client = instructor.patch(openai.OpenAI())


class ComparableSale(BaseModel):
    address: str
    sale_price: int
    price_per_sqft: float
    bedrooms: int
    bathrooms: float
    sqft: int
    days_on_market: int
    similarity_score: float = Field(ge=0, le=100)


class CompsAnalysis(BaseModel):
    comparable_sales: list[ComparableSale]
    median_comp_price: int
    median_price_per_sqft: float
    analyst_notes: str


class MarketTrend(BaseModel):
    area: str
    ninety_day_price_change_pct: float
    median_days_on_market: int
    list_to_sale_ratio: float
    absorption_rate_months: float
    market_direction: Literal["appreciating", "stable", "declining"]
    demand_signal: Literal["strong", "moderate", "weak"]


class ValuationReport(BaseModel):
    property_address: str
    estimated_market_value: int
    confidence_band_low: int
    confidence_band_high: int
    price_per_sqft_estimate: float
    recommendation: Literal["buy", "hold", "sell"]
    recommendation_rationale: str
    key_risks: list[str]
    report_quality: Literal["high", "medium", "low"]


def build_tasks(comps_analyst, trend_analyst, report_writer, property_data: dict):
    task1 = Task(
        description=f"""Analyse the following property and identify the 5 most comparable
recent sales within a 1-mile radius. Score each comp on similarity (0-100).

Property Data: {property_data}

Focus on: matching property type, size (±20%), bedroom/bathroom count,
age (±10 years), and location proximity. Calculate median comp price and
price-per-sqft from your selected comps.""",
        agent=comps_analyst,
        expected_output="Structured comps analysis with 5 comparable sales and median metrics",
    )

    task2 = Task(
        description="""Using the property location from Task 1, analyse the current market
conditions for that area over the past 90 days.

Calculate: median price trend, days-on-market trend, list-to-sale price ratio,
absorption rate (months of supply), and classify the market direction.
Determine the demand signal strength.""",
        agent=trend_analyst,
        expected_output="Market trend analysis with directional signal and absorption rate",
        context=[task1],
    )

    task3 = Task(
        description="""Using the comps analysis (Task 1) and market trend data (Task 2),
produce a complete investor-grade property valuation report.

Include:
- Estimated market value with confidence band (±%)
- Price per sqft estimate vs area median
- Explicit buy/hold/sell recommendation with rationale
- Top 3 investment risks

Be precise and data-driven. Do not speculate beyond the evidence.""",
        agent=report_writer,
        expected_output="Complete valuation report with recommendation and risk summary",
        context=[task1, task2],
    )

    return task1, task2, task3
