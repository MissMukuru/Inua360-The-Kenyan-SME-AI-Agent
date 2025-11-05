from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import numpy as np
import joblib
from pathlib import Path

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
def preprocess_funding(df: pd.DataFrame):
    bool_cols = ["AML_risk_flag", "has_pitch_deck", "registered_business",
                 "female_owned", "employee_contracts_verified"]
    for col in bool_cols:
        df[col] = df[col].astype(int)

    # Feature engineering
    df["expense_ratio"] = (df["expenses_total"] / df["annual_revenue"]).replace([np.inf, -np.inf], 0).fillna(0)
    df["employee_efficiency"] = (df["annual_revenue"] - df["expenses_total"]) / (df["num_employees"] + 1)
    df["financial_health_index"] = df["cash_flow_score"]*0.4 + df["credit_score"]*0.3 + df["profit_to_expense_ratio"]*0.3
    df["compliance_score"] = df["financial_transparency_score"]*0.4 + df["bookkeeping_quality"]*0.3 + df["data_protection_score"]*0.2 + (1 - df["AML_risk_flag"])*0.1
    df["market_resilience"] = df["traction_score"]*0.4 + df["digital_spending_ratio"]*0.3 + df["customer_retention_rate"]*0.3

    # One-hot encode categorical columns
    categorical_cols = ['tech_adoption_level', 'sector', 'country', 'region', 
                        'prior_investment', 'tax_compliance_status', 'regulatory_license_status',
                        'remote_work_policy']
    df = pd.get_dummies(df, columns=categorical_cols, drop_first=False)

    # Align with training columns
    df = df.reindex(columns=funding_features, fill_value=0)
    return df

def preprocess_compliance(df: pd.DataFrame):
    bool_cols = ["AML_risk_flag", "has_pitch_deck", "registered_business",
                 "female_owned", "employee_contracts_verified"]
    for col in bool_cols:
        df[col] = df[col].astype(int)

    # One-hot encode categorical columns
    categorical_cols = ['tech_adoption_level', 'sector', 'country', 'region', 
                        'prior_investment', 'tax_compliance_status', 'regulatory_license_status',
                        'remote_work_policy']
    df = pd.get_dummies(df, columns=categorical_cols, drop_first=False)

    # Align with training columns
    df = df.reindex(columns=compliance_features, fill_value=0)
    return df

def preprocess_growth(df: pd.DataFrame):
    # Boolean features
    bool_cols = ["AML_risk_flag", "has_pitch_deck", "registered_business",
                 "female_owned", "employee_contracts_verified"]
    for col in bool_cols:
        df[col] = df[col].astype(int)

    # Feature engineering
    df["expense_ratio"] = (df["expenses_total"] / df["annual_revenue"]).replace([np.inf, -np.inf], 0).fillna(0)
    df["employee_efficiency"] = (df["annual_revenue"] - df["expenses_total"]) / (df["num_employees"] + 1)
    df["financial_health_index"] = df["cash_flow_score"]*0.4 + df["credit_score"]*0.3 + df["profit_to_expense_ratio"]*0.3
    df["compliance_score"] = df["financial_transparency_score"]*0.4 + df["bookkeeping_quality"]*0.3 + df["data_protection_score"]*0.2 + (1 - df["AML_risk_flag"])*0.1
    df["market_resilience"] = df["traction_score"]*0.4 + df["digital_spending_ratio"]*0.3 + df["customer_retention_rate"]*0.3

    # Add dummy target columns used during training
    for col in ["funding_stage", "compliance_risk_level"]:
        if col not in df.columns:
            df[col] = 0

    # One-hot encode categorical columns
    categorical_cols = ['tech_adoption_level', 'sector', 'country', 'region', 
                        'prior_investment', 'tax_compliance_status', 'regulatory_license_status',
                        'remote_work_policy']
    df = pd.get_dummies(df, columns=categorical_cols, drop_first=False)

    # Reindex to match preprocessed training features
    df = df.reindex(columns=growth_features, fill_value=0)
    return df

# -----------------------
# API endpoints
# -----------------------
@app.post("/predict/funding")
def predict_funding(input: SMEInput):
    df = pd.DataFrame([input.dict()])
    df = preprocess_funding(df)
    prediction = funding_model.predict(df)[0]
    return {"funding_prediction": prediction}

@app.post("/predict/compliance")
def predict_compliance(input: SMEInput):
    df = pd.DataFrame([input.dict()])
    df = preprocess_compliance(df)
    prediction = compliance_model.predict(df)[0]
    return {"compliance_prediction": prediction}

@app.post("/predict/growth")

def predict_growth(input: SMEInput):
    df = pd.DataFrame([input.dict()])

    # Feature engineering (same as before)
    df = preprocess_growth(df)

    # Load model components
    model_data = joblib.load(GROWTH_MODEL_PATH)
    model = model_data["model"]
    encoder = model_data["encoder"]
    scaler = model_data["scaler"]

    # Split columns like in training
    categorical_cols = encoder.feature_names_in_.tolist()
    numeric_cols = scaler.feature_names_in_.tolist()

    # Encode and scale
    X_cat = encoder.transform(df[categorical_cols])
    X_num = scaler.transform(df[numeric_cols])
    X_processed = np.hstack([X_cat, X_num])

    # Predict
    prediction = model.predict(X_processed)[0]
    return {"growth_prediction": float(prediction)}

# -----------------------
# Run the server
# -----------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
