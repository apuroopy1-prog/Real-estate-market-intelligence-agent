"""api.py — FastAPI endpoint"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.crew import run_valuation_crew

app = FastAPI(title="Real Estate Market Intelligence Agent")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


class PropertyRequest(BaseModel):
    address: str
    property_type: str
    bedrooms: int
    bathrooms: float
    sqft: int
    year_built: int
    asking_price: int
    condition: str = "good"
    additional_notes: dict = {}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/valuate")
def valuate_property(req: PropertyRequest):
    try:
        result = run_valuation_crew(req.model_dump())
        return result
    except Exception as e:
        raise HTTPException(500, str(e))
