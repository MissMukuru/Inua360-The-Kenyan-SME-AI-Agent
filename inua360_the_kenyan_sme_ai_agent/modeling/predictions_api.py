from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
import httpx
import asyncio
import os 
from loguru import logger
from openai import OpenAI
import dotenv

dotenv.load_dotenv()
llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def llm_advice(system_prompt: str, user_prompt: str):
    try:
        response = llm.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
            max_tokens=500
        )
        content = response.choices[0].message.content
        return content
    except Exception as e:
        logger.error(f"LLM advice generation failed: {e}")
        return "Error generating advice."

# -----------------------
# JSON Serialization Fix
# -----------------------
def make_json_serializable(obj):
    if isinstance(obj, np.generic):
        return obj.item()
    elif isinstance(obj, dict):
        return {k: make_json_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [make_json_serializable(v) for v in obj]
    else:
        return obj

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
app = FastAPI(
    title="Inua360 SME AI Agent",
    description="Public API for SME funding and compliance predictions.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


# -----------------------
# n8n webhook integration
# -----------------------
N8N_WEBHOOK_URL="https://abby218.app.n8n.cloud/webhook/sme-data"

async def send_to_n8n(payload: dict):
    """Send payload to n8n webhook with graceful error handling."""
    payload = make_json_serializable(payload)
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(N8N_WEBHOOK_URL, json=payload, timeout=10)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"n8n returned HTTP error {e.response.status_code}: {e.response.text}")
        except httpx.RequestError as e:
            print(f"Error connecting to n8n: {e}")
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

def preprocess_funding(df): return base_preprocessing(df).reindex(columns=funding_features, fill_value=0)
def preprocess_compliance(df): return base_preprocessing(df).reindex(columns=compliance_features, fill_value=0)
def preprocess_growth(df): return base_preprocessing(df).reindex(columns=growth_features, fill_value=0)

# -----------------------
# API endpoints
# -----------------------
@app.post("/predict/funding")
async def predict_funding(input: SMEInput):
    df = preprocess_funding(pd.DataFrame([input.model_dump()]))
    prediction = make_json_serializable(funding_model.predict(df)[0])

    advice = await llm_advice(
        "You are a senior SME funding advisor.",
        f"SME input: {input.model_dump()}\nFunding Prediction: {prediction}"
    )

    result = {"funding_prediction": prediction, "funding_advice": advice}
    asyncio.create_task(send_to_n8n({"model": "funding", "inputs": input.dict(), "prediction": prediction}))
    return make_json_serializable(result)

@app.post("/predict/compliance")
async def predict_compliance(input: SMEInput):
    df = preprocess_compliance(pd.DataFrame([input.dict()]))
    prediction = make_json_serializable(compliance_model.predict(df)[0])

    advice = await llm_advice(
        "You are a compliance expert for SMEs.",
        f"SME input: {input.dict()}\nCompliance Prediction: {prediction}"
    )

    result = {"compliance_prediction": prediction, "compliance_advice": advice}
    asyncio.create_task(send_to_n8n({"model": "compliance", "inputs": input.dict(), "prediction": prediction}))
    return make_json_serializable(result)

@app.post("/predict/growth")
async def predict_growth(input: SMEInput):
    df = preprocess_growth(pd.DataFrame([input.dict()]))
    prediction = make_json_serializable(growth_model.predict(df)[0])

    advice = await llm_advice(
        "You are a growth strategist for SMEs.",
        f"SME input: {input.dict()}\nGrowth Prediction: {prediction}"
    )

    result = {"growth_prediction": prediction, "growth_advice": advice}
    asyncio.create_task(send_to_n8n({"model": "growth", "inputs": input.dict(), "prediction": prediction}))
    return make_json_serializable(result)

@app.post("/predict/sme")
async def predict_sme(input: SMEInput):
    df = pd.DataFrame([input.dict()])

    funding_pred = make_json_serializable(funding_model.predict(preprocess_funding(df))[0])
    compliance_pred = make_json_serializable(compliance_model.predict(preprocess_compliance(df))[0])
    growth_pred = make_json_serializable(growth_model.predict(preprocess_growth(df))[0])

    predictions = {"funding": funding_pred, "compliance": compliance_pred, "growth": growth_pred}

    system_prompt = """
    You are the Inua360 AI SME Advisor.

    - A short executive summary
    - A unique, creative “Inua360 Insight” 
    - Funding outlook (using the model predictions)
    - Compliance interpretation
    - Growth projection
    - Risk radar: identify top 3 risks and mitigation strategies
    - Innovator pitch: a short persuasive pitch for this SME
    - Strategic roadmap: 3 actionable steps for next 6 months
    - A 14-day action plan
    - A Kenya SME opportunity angle
    
    Use clean Markdown: **bold**, bullet points, short paragraphs.
Do NOT use hashes (#), slashes (/), HTML tags, or weird symbols.
Keep it readable for a modern frontend UI.
"""
    user_prompt = f"""
    SME Input: {input.dict()}
    Model Predictions:
      - Funding: {funding_pred}
      - Compliance: {compliance_pred}
      - Growth: {growth_pred}

    Generate a single combined business advisory report.
    """

    overall_advice = await llm_advice(system_prompt, user_prompt)
    # Send to n8n in a background thread, do not await it
    asyncio.create_task(send_to_n8n(make_json_serializable({
        "model": "combined_sme",
        "inputs": input.dict(),
        "predictions": predictions,
        "overall_advice": overall_advice
    })))

    # Return immediately to the client
    return make_json_serializable({
        "predictions": predictions,
        "overall_advice": overall_advice
    })


# -----------------------
# Run the server
# -----------------------
if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
