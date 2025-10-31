import json
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import lightgbm as lgb
from loguru import logger
from dotenv import load_dotenv
import typer
import warnings
from inua360_the_kenyan_sme_ai_agent.config import MODELS_DIR, METRICS_DIR, PROCESSED_DATA_DIR

warnings.filterwarnings("ignore")
app = typer.Typer()

@app.command()
def main(
    input_path: Path = PROCESSED_DATA_DIR / "sme_revenue_growth_synthetic_processed.csv",
    growth_model_path: Path = MODELS_DIR / "growth_model.pkl",
    metrics_path: Path = METRICS_DIR / "growth_model_metrics.json",
    test_size: float = 0.2,
    random_state: int = 42
):
    """Train LightGBM to predict revenue_growth_rate."""
    
    logger.info(f"Loading data from {input_path}...")
    df = pd.read_csv(input_path)
    df.columns = df.columns.str.strip().str.lower()
    logger.success(f"Data loaded with shape {df.shape}")
    
    df = df.dropna(subset=["revenue_growth_rate"])
    
    X = df.drop(columns=["revenue_growth_rate"])
    y = df["revenue_growth_rate"]
    
    categorical_cols = X.select_dtypes(include=["object"]).columns.tolist()
    numeric_cols = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
    
    logger.info(f"Categorical columns: {categorical_cols}")
    logger.info(f"Numeric columns: {numeric_cols}")
    
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
            ("num", StandardScaler(), numeric_cols)
        ]
    )
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    
    model = lgb.LGBMRegressor(
        n_estimators=500,
        learning_rate=0.01,
        max_depth=12,
        num_leaves=31,
        min_child_samples=20,
        reg_alpha=0.1,
        reg_lambda=0.1,
        random_state=random_state
    )
    
    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("model", model)
    ])
    
    logger.info("Training LightGBM model...")
    pipeline.fit(X_train, y_train)
    
    y_pred = pipeline.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    
    metrics = {"R2": round(r2, 4), "RMSE": round(rmse, 4), "MAE": round(mae, 4)}
    logger.success(f"Training completed. Metrics: {metrics}")
    
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    METRICS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, growth_model_path)
    logger.success(f"Model saved to {growth_model_path}")
    
    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=4)
    logger.success(f"Metrics saved to {metrics_path}")

if __name__ == "__main__":
    app()
