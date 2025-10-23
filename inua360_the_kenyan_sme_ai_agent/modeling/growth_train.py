import json
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.linear_model import Lasso, LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from xgboost import XGBRegressor
from loguru import logger
import typer

from inua360_the_kenyan_sme_ai_agent.config import METRICS_DIR, MODELS_DIR, PROCESSED_DATA_DIR, REPORTS_DIR

app = typer.Typer()


@app.command()
def main(
    growth_model_path: Path = MODELS_DIR / "growth_model.pkl",
    metrics_path: Path = METRICS_DIR / "growth_model_metrics.JSON",
):
    """
    Train and evaluate regression models for predicting growth_last_yr (% growth in revenue).
    The best model (based on R^2 score) 
    """

    logger.info(f"Loading Preprocessed Growth Training and Testing data...")
    
    train_path = PROCESSED_DATA_DIR / "growth_train.csv"
    test_path = PROCESSED_DATA_DIR / "growth_test.csv"
    
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)
    train_df.columns = train_df.columns.str.strip()
    test_df.columns = test_df.columns.str.strip()

    X_train = train_df.drop(columns=["growth_last_yr"])
    y_train = train_df["growth_last_yr"]
    
    X_test = test_df.drop(columns=["growth_last_yr"])
    y_test = test_df["growth_last_yr"]

    logger.info(f" Training data shape: {X_train.shape}, Test data shape: {X_test.shape}")

    # Define candidate models and parameter grids
    models = {
        "LinearRegression": (LinearRegression(), {}),
        "Ridge": (Ridge(), {"alpha": [0.1, 1.0, 10.0]}),
        "Lasso": (Lasso(), {"alpha": [0.001, 0.01, 0.1, 1.0]}),
        "RandomForest": (
            RandomForestRegressor(random_state=42),
            {
                "n_estimators": [50, 100],
                "max_depth": [5, 10, None],
            },
        ),
        "GradientBoosting": (
            GradientBoostingRegressor(random_state=42),
            {
                "n_estimators": [100, 200],
                "learning_rate": [0.05, 0.1],
                "max_depth": [3, 5],
            },
        ),
        "XGBoost": (
            XGBRegressor(random_state=42, objective="reg:squarederror"),
            {
                "n_estimators": [50, 100],
                "learning_rate": [0.01, 0.05],
                "max_depth": [2 ,3],
                "subsample": [0.7 , 0.8],
            },
        ),
    }

    best_model = None
    best_name = None
    best_r2 = -np.inf
    all_metrics = {}

    # Train and evaluate each model
    for name, (model, params) in models.items():
        logger.info(f" Training model: {name}")

        if params:
            grid = GridSearchCV(model, params, cv=3, n_jobs=-1, scoring="r2")
            grid.fit(X_train, y_train)
            best_estimator = grid.best_estimator_
        else:
            model.fit(X_train, y_train)
            best_estimator = model

        y_pred = best_estimator.predict(X_test)
        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))

        all_metrics[name] = {
            "R2": round(r2, 4),
            "MAE": round(mae, 4),
            "RMSE": round(rmse, 4),
        }

        logger.info(f"{name} -> R2: {r2:.4f}, MAE: {mae:.4f}, RMSE: {rmse:.4f}")

        if r2 > best_r2:
            best_r2 = r2
            best_name = name
            best_model = best_estimator

    logger.success(f"Best Model: {best_name} with R² = {best_r2:.4f}")

    # Ensure metrics directory exists
    metrics_path.parent.mkdir(parents=True, exist_ok=True)

    # Save metrics as JSON
    with open(metrics_path, "w") as f:
        json.dump(all_metrics, f, indent=4)
    logger.success(f" Metrics saved to {metrics_path}")

    # Save best model
    joblib.dump(best_model, growth_model_path)
    logger.success(f"Best model saved to {growth_model_path}")


if __name__ == "__main__":
    app()