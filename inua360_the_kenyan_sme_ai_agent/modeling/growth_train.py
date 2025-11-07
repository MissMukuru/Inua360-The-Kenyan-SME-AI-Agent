import json
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from xgboost import XGBRegressor
from loguru import logger
import typer
import warnings

from inua360_the_kenyan_sme_ai_agent.config import MODELS_DIR, METRICS_DIR, PROCESSED_DATA_DIR

app = typer.Typer()
warnings.filterwarnings("ignore")

@app.command()
def main(
    growth_model_path: Path = MODELS_DIR / "growth_model.pkl",
    growth_features_path: Path = MODELS_DIR / "growth_features.pkl",
    growth_metrics_path: Path = METRICS_DIR / "growth_model_metrics.json",
    input_path: Path = PROCESSED_DATA_DIR / "training.csv"
):
    logger.info("Loading dataset...")
    data = pd.read_csv(input_path)
    data.columns = data.columns.str.strip().str.lower()

    # Drop missing target rows
    data = data.dropna(subset=["revenue_growth_rate"])
    X = data.drop(columns=["revenue_growth_rate"])
    y = data["revenue_growth_rate"]

    # One-hot encode categorical features
    X = pd.get_dummies(X, drop_first=True)

    # Standardize numeric columns
    numeric_cols = X.select_dtypes(include=np.number).columns
    scaler = StandardScaler()
    X[numeric_cols] = scaler.fit_transform(X[numeric_cols])

    # Save feature list for use during prediction
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(X.columns.tolist(), growth_features_path)
    logger.success(f"Growth feature list saved to {growth_features_path}")

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Define model
    model = XGBRegressor(
        n_estimators=500,
        learning_rate=0.05,
        max_depth=8,
        subsample=0.8,
        colsample_bytree=0.8,
        reg_alpha=0.1,
        reg_lambda=0.1,
        random_state=42
    )

    logger.info("Training XGBoost Regressor...")
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)

    metrics = {"R2": round(r2, 4), "RMSE": round(rmse, 4), "MAE": round(mae, 4)}

    logger.success(f"Model training complete with metrics: {metrics}")

    # Save model
    joblib.dump(model, growth_model_path)
    logger.success(f"Growth model saved to {growth_model_path}")

    # Save metrics
    METRICS_DIR.mkdir(parents=True, exist_ok=True)
    with open(growth_metrics_path, "w") as f:
        json.dump(metrics, f, indent=4)
    logger.success(f"Metrics saved to {growth_metrics_path}")

if __name__ == "__main__":
    app()
