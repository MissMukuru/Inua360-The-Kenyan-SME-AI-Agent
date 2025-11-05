from pathlib import Path
from sklearn.preprocessing import StandardScaler
from loguru import logger
import typer
import pandas as pd
import numpy as np

from inua360_the_kenyan_sme_ai_agent.config import EXTERNAL_DATA_DIR, PROCESSED_DATA_DIR

app = typer.Typer()


@app.command()
def main(
    input_path: Path = PROCESSED_DATA_DIR / "african_sme_dataset.csv",
    output_path: Path = PROCESSED_DATA_DIR / "training.csv",
):
    # Load data
    data = pd.read_csv(input_path)
    data.columns = data.columns.str.strip()
    data = data.drop(columns=["company_id"], errors="ignore")
    logger.info(f"Loaded dataset from {input_path}")

    # Feature Engineering
    data["expense_ratio"] = (
        data["expenses_total"] / data["annual_revenue"]
    ).replace([np.inf, -np.inf], 0).fillna(0)

    data["employee_efficiency"] = (
        (data["annual_revenue"] - data["expenses_total"]) / (data["num_employees"] + 1)
    )

    data["financial_health_index"] = (
        data["cash_flow_score"] * 0.4 +
        data["credit_score"] * 0.3 +
        data["profit_to_expense_ratio"] * 0.3
    )

    data["compliance_score"] = (
        data["financial_transparency_score"] * 0.4 +
        data["bookkeeping_quality"] * 0.3 +
        data["data_protection_score"] * 0.2 +
        (1 - data["AML_risk_flag"]) * 0.1
    )

    data["market_resilience"] = (
        data["traction_score"] * 0.4 +
        data["digital_spending_ratio"] * 0.3 +
        data["customer_retention_rate"] * 0.3
    )

    # Targets
    targets = ["funding_stage", "revenue_growth_rate", "compliance_risk_level"]
    targets_df = data[targets].copy()

    # Remove targets from feature set
    data_features = data.drop(columns=targets, errors="ignore")

    # Convert boolean/binary columns
    bool_cols = [
        "has_pitch_deck", "registered_business", "female_owned",
        "employee_contracts_verified", "AML_risk_flag"
    ]

    for col in bool_cols:
        if col in data_features.columns:
            data_features[col] = data_features[col].astype(int)

    # Encode categorical columns
    categorical_cols = data_features.select_dtypes(include="object").columns
    data_features = pd.get_dummies(data_features, columns=categorical_cols, drop_first=True)
    logger.info("Categorical features encoded")

    # Numeric columns to scale
    numeric_cols_to_scale = [
        "years_in_operation", "annual_revenue", "expenses_total",
        "num_employees", "avg_employee_salary", "customer_growth_rate",
        "customer_retention_rate", "digital_spending_ratio",
        "profit_to_expense_ratio", "cash_flow_score", "credit_score",
        "traction_score", "bookkeeping_quality", "data_protection_score",
        "financial_transparency_score", "expense_ratio", "employee_efficiency",
        "financial_health_index", "compliance_score", "market_resilience"
    ]
    numeric_cols_to_scale = [col for col in numeric_cols_to_scale if col in data_features.columns]

    # Log transform
    data_features[numeric_cols_to_scale] = data_features[numeric_cols_to_scale].apply(
        lambda col: np.log1p(col - col.min() + 1)
    )

    # Standardization
    scaler = StandardScaler()
    data_features[numeric_cols_to_scale] = scaler.fit_transform(data_features[numeric_cols_to_scale])
    logger.info("Numeric features log-transformed and standardized")

    # Reattach targets
    data_final = pd.concat([data_features, targets_df], axis=1)

    # Save output
    data_final.to_csv(output_path, index=False)
    logger.success(f"Processed dataset saved at {output_path}")


if __name__ == "__main__":
    app()
