import json
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from loguru import logger
from dotenv import load_dotenv
import typer

from inua360_the_kenyan_sme_ai_agent.config import MODELS_DIR, PROCESSED_DATA_DIR, PROJ_ROOT

app = typer.Typer()

PREDICTIONS_DIR = PROJ_ROOT / "reports" / "predictions"
PREDICTIONS_DIR.mkdir(parents=True, exist_ok=True)

@app.command()
def predict(
    model_path: Path = MODELS_DIR / "growth_model.pkl",
    single_input: str = None,
):
    """Predict revenue growth for a single SME from JSON input."""
    
    logger.info(f"Loading model from {model_path}...")
    pipeline = joblib.load(model_path)
    logger.success("Model loaded successfully.")

    if single_input is None:
        logger.error("No input provided. Use --single-input with JSON string.")
        raise typer.Exit()

    logger.info("Parsing single SME input...")
    data_dict = json.loads(single_input)
    
    expected_columns = [
        'num_employees', 'annual_revenue', 'avg_employee_salary', 'expenses_total',
        'customer_growth_rate', 'customer_retention_rate', 'digital_spending_ratio',
        'years_in_operation', 'profit_to_expense_ratio', 'region', 'sector',
        'tech_adoption_level', 'remote_work_policy', 'revenue_growth_rate'
    ]
    
    for col in expected_columns:
        if col not in data_dict:
            if col in ['region', 'sector', 'tech_adoption_level', 'remote_work_policy']:
                data_dict[col] = "Unknown"
            else:
                data_dict[col] = np.nan

    X = pd.DataFrame([data_dict], columns=expected_columns)
    logger.info(f"Input data shape: {X.shape}")

    predictions = pipeline.predict(X)
    X["predicted_revenue_growth"] = predictions
    logger.success("Predictions generated successfully.")

    output_path = PREDICTIONS_DIR / "predicted_growth.json"
    X[['predicted_revenue_growth']].to_json(output_path, orient='records', indent=4)
    logger.success(f"Predictions saved to {output_path}")

    print(json.dumps(X[['predicted_revenue_growth']].to_dict(orient='records'), indent=4))

if __name__ == "__main__":
    app()
