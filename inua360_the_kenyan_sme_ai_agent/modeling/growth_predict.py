import pandas as pd
import numpy as np
import joblib
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from loguru import logger
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import typer
from inua360_the_kenyan_sme_ai_agent.config import MODELS_DIR, PROCESSED_DATA_DIR, INTERIM_DATA_DIR, REPORTS_DIR 


app = typer.Typer()

@app.command()
def main(
    model_path: Path = MODELS_DIR / "growth_model.pkl",
    input_path: Path = INTERIM_DATA_DIR / "new_smes_data.csv",
    output_path: Path = PROCESSED_DATA_DIR / "growth_predictions.csv",
):
    """
    Load the trained model and make predictions on the test set.
    """

    logger.info(f"Loading model from {model_path}")
    model = joblib.load(model_path)
    logger.success("Model loaded successfully.")

    logger.info(f"Loading data from {input_path}")
    df = pd.read_csv(input_path)
    df.columns = df.columns.str.strip()

    has_target = "growth_last_yr" in df.columns
    if has_target:
        X = df.drop(columns=["growth_last_yr"])
        y_true = df["growth_last_yr"]
    else:
        X = df

    logger.info("Making predictions...")
    y_pred = model.predict(X)
    df["predicted_growth"] = y_pred


    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.success(f"Predictions saved to {output_path}")

    if has_target:
        r2 = r2_score(y_true, y_pred)
        mae = mean_absolute_error(y_true, y_pred)
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        logger.success(f"Metrics -> R²: {r2:.4f}, MAE: {mae:.4f}, RMSE: {rmse:.4f}")

if __name__ == "__main__":
    app()