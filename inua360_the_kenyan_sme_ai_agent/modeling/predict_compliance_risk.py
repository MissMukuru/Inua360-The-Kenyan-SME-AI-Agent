import json
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from loguru import logger
import typer

from inua360_the_kenyan_sme_ai_agent.config import MODELS_DIR, PROJ_ROOT

app = typer.Typer()

PREDICTIONS_DIR = PROJ_ROOT / "reports" / "predictions"
PREDICTIONS_DIR.mkdir(parents=True, exist_ok=True)

@app.command()
def predict(
    model_path: Path = MODELS_DIR / "best_compliance_model.pkl",
    single_input: str = None,
):
    """Predict compliance risk for a single SME from JSON input."""
    
    logger.info(f"Loading model from {model_path}...")
    pipeline = joblib.load(model_path)
    logger.success("Model loaded successfully.")

    if single_input is None:
        logger.error("No input provided. Use --single-input with JSON string.")
        raise typer.Exit()

    logger.info("Parsing single SME input...")
    data_dict = json.loads(single_input)
    
    expected_columns = [
        'company_id', 'country', 'sector', 'employees', 'annual_revenue',
        'tech_adoption_level', 'main_challenges', 'digital_tools_used',
        'growth_last_year', 'female_owned', 'remote_work_policy'
    ]

    for col in expected_columns:
        if col not in data_dict:
            if col in ['country', 'sector', 'tech_adoption_level', 'main_challenges',
                       'digital_tools_used', 'remote_work_policy', 'female_owned']:
                data_dict[col] = "Unknown"
            else:
                data_dict[col] = np.nan

    X = pd.DataFrame([data_dict], columns=expected_columns)
    logger.info(f"Input data shape: {X.shape}")

    predictions = pipeline.predict(X)
    X["predicted_compliance_risk"] = predictions
    logger.success("Predictions generated successfully.")

    output_path = PREDICTIONS_DIR / "predicted_compliance.json"
    X[['predicted_compliance_risk']].to_json(output_path, orient='records', indent=4)
    logger.success(f"Predictions saved to {output_path}")

    print(json.dumps(X[['predicted_compliance_risk']].to_dict(orient='records'), indent=4))

if __name__ == "__main__":
    app()
