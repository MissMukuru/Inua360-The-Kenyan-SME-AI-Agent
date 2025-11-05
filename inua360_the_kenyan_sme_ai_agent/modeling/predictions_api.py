from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
import httpx
import asyncio

# -----------------------
# Paths
# -----------------------
MODELS_DIR = Path("models")

FUNDING_MODEL_PATH = MODELS_DIR / "best_funding_model.pkl"
COMPLIANCE_MODEL_PATH = MODELS_DIR / "best_compliance_risk_level_model.pkl"
GROWTH_MODEL_PATH = MODELS_DIR / "growth_model.pkl"

FUNDING_FEATURES_PATH = MODELS_DIR / "funding_features.pkl"
COMPLIANCE_FEATURES_PATH = MODELS_DIR / "compliance_features.pkl"
GROWTH_FEATURES_PATH = MODELS_DIR / "growth_features.pkl"

# -----------------------
# Load models and features
# -----------------------
funding_model = joblib.load(FUNDING_MODEL_PATH)
compliance_model = joblib.load(COMPLIANCE_MODEL_PATH)
growth_model = joblib.load(GROWTH_MODEL_PATH)

funding_features = joblib.load(FUNDING_FEATURES_PATH)
compliance_features = joblib.load(COMPLIANCE_FEATURES_PATH)
growth_features = joblib.load(GROWTH_FEATURES_PATH)

# -----------------------
# FastAPI app
# -----------------------
app = FastAPI(title="SME AI Prediction API")

# -----------------------
# n8n webhook integration
# -----------------------
N8N_WEBHOOK_URL = "https://abby218.app.n8n.cloud/webhook/f71a7d4c-dff3-42e7-b081-a02fad74b56d"

async def send_to_n8n(payload: dict):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(N8N_WEBHOOK_URL, json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error sending to n8n: {e}")
            return None

# -----------------------
# Input schema
# -----------------------
class SMEInput(BaseModel):
    annual_revenue: float
    expenses_total: float
    num_employees: int
    avg_employee_salary: float
    customer_growth_rate: float
    customer_retention_rate: float
    digital_spending_ratio: float
    profit_to_expense_ratio: float
    cash_flow_score: float
    credit_score: float
    traction_score: float
    bookkeeping_quality: float
    data_protection_score: float
    financial_transparency_score: float
    AML_risk_flag: int
    has_pitch_deck: int
    registered_business: int
    female_owned: int
    employee_contracts_verified: int
    years_in_operation: float
    tech_adoption_level: str
    sector: str
    country: str
    region: str
    prior_investment: str
    tax_compliance_status: str
    regulatory_license_status: str
    remote_work_policy: str

# -----------------------
# Preprocessing functions
# -----------------------
def base_preprocessing(df: pd.DataFrame) -> pd.DataFrame:
    """Shared feature engineering for all endpoints."""
    bool_cols = [
        "AML_risk_flag", "has_pitch_deck", "registered_business",
        "female_owned", "employee_contracts_verified"
    ]
    for col in bool_cols:
        df[col] = df[col].astype(int)

    df["expense_ratio"] = (df["expenses_total"] / df["annual_revenue"]).replace([np.inf, -np.inf], 0).fillna(0)
    df["employee_efficiency"] = (df["annual_revenue"] - df["expenses_total"]) / (df["num_employees"] + 1)
    df["financial_health_index"] = (
        df["cash_flow_score"] * 0.4 +
        df["credit_score"] * 0.3 +
        df["profit_to_expense_ratio"] * 0.3
    )
    df["compliance_score"] = (
        df["financial_transparency_score"] * 0.4 +
        df["bookkeeping_quality"] * 0.3 +
        df["data_protection_score"] * 0.2 +
        (1 - df["AML_risk_flag"]) * 0.1
    )
    df["market_resilience"] = (
        df["traction_score"] * 0.4 +
        df["digital_spending_ratio"] * 0.3 +
        df["customer_retention_rate"] * 0.3
    )

    categorical_cols = [
        'tech_adoption_level', 'sector', 'country', 'region',
        'prior_investment', 'tax_compliance_status',
        'regulatory_license_status', 'remote_work_policy'
    ]
    df = pd.get_dummies(df, columns=categorical_cols, drop_first=False)
    return df

def preprocess_funding(df: pd.DataFrame) -> pd.DataFrame:
    df = base_preprocessing(df)
    df = df.reindex(columns=funding_features, fill_value=0)
    return df

def preprocess_compliance(df: pd.DataFrame) -> pd.DataFrame:
    df = base_preprocessing(df)
    df = df.reindex(columns=compliance_features, fill_value=0)
    return df

def preprocess_growth(df: pd.DataFrame) -> pd.DataFrame:
    df = base_preprocessing(df)
    df = df.reindex(columns=growth_features, fill_value=0)
    return df

# -----------------------
# API endpoints
# -----------------------
@app.post("/predict/funding")
async def predict_funding(input: SMEInput):
    df = pd.DataFrame([input.dict()])
    df = preprocess_funding(df)
    prediction = funding_model.predict(df)[0]
    
    result = {"funding_prediction": float(prediction) if isinstance(prediction, (int, float, np.floating)) else str(prediction)}
    
    # Send to n8n webhook
    payload = {
        "model": "funding",
        "inputs": input.dict(),
        "prediction": result["funding_prediction"]
    }
    asyncio.create_task(send_to_n8n(payload))
    
    return result

@app.post("/predict/compliance")
async def predict_compliance(input: SMEInput):
    df = pd.DataFrame([input.dict()])
    df = preprocess_compliance(df)
    prediction = compliance_model.predict(df)[0]

    result = {"compliance_prediction": float(prediction) if isinstance(prediction, (int, float, np.floating)) else str(prediction)}
    
    # Send to n8n webhook
    payload = {
        "model": "compliance",
        "inputs": input.dict(),
        "prediction": result["compliance_prediction"]
    }
    asyncio.create_task(send_to_n8n(payload))
    
    return result

@app.post("/predict/growth")
async def predict_growth(input: SMEInput):
    df = pd.DataFrame([input.dict()])
    df = preprocess_growth(df)
    prediction = growth_model.predict(df)[0]

    result = {"growth_prediction": float(prediction) if isinstance(prediction, (int, float, np.floating)) else str(prediction)}
    
    # Send to n8n webhook
    payload = {
        "model": "growth",
        "inputs": input.dict(),
        "prediction": result["growth_prediction"]
    }
    asyncio.create_task(send_to_n8n(payload))
    
    return result

# -----------------------
# Run the server
# -----------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
