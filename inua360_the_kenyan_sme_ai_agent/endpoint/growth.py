from fastapi import APIRouter, FastAPI
from pydantic import BaseModel
from typing import Optional
import pandas as pd
import numpy as np  
import joblib
from pathlib import Path
from inua360_the_kenyan_sme_ai_agent.config import MODELS_DIR
import os

router = APIRouter()

pipeline = joblib.load(MODELS_DIR / "growth_model.pkl")

class SMEFeatures(BaseModel):
    num_employees: Optional[int] = None
    annual_revenue: Optional[float] = None
    avg_employee_salary: Optional[float] = None
    expenses_total: Optional[float] = None
    customer_growth_rate: Optional[float] = None
    customer_retention_rate: Optional[float] = None
    digital_spending_ratio: Optional[float] = None
    years_in_operation: Optional[int] = None
    profit_to_expense_ratio: Optional[float] = None
    region: Optional[str] = None
    sector: Optional[str] = None
    tech_adoption_level: Optional[str] = None
    remote_work_policy: Optional[str] = None

@router.post("/predict-growth")
def predict_growth(features: SMEFeatures):
    input_df = pd.DataFrame([features.dict()])
    input_df = input_df.replace({None: np.nan})
    pred = pipeline.predict(input_df)
    return {"predicted_revenue_growth": float(pred[0])}