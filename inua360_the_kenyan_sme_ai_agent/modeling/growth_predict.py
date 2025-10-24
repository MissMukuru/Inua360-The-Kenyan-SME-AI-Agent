# import pandas as pd
# import joblib
# from pathlib import Path
# from loguru import logger
# from inua360_the_kenyan_sme_ai_agent.config import MODELS_DIR, PROCESSED_DATA_DIR, REPORTS_DIR

# class GrowthPredictor:
#     def __init__(self, model_path: Path = MODELS_DIR / "growth_model.pkl"):
#         self.model_path = model_path
#         self.model = None

#     def load_model(self):
#         """Load the trained growth model."""
#         if not self.model_path.exists():
#             raise FileNotFoundError(f"Model file not found at: {self.model_path}")
#         self.model = joblib.load(self.model_path)
#         logger.info(f"Model loaded from {self.model_path}")

#     def predict(self, input_df: pd.DataFrame):
#         """Make predictions for a DataFrame with the same features as training."""
#         if self.model is None:
#             raise RuntimeError("Model not loaded. Call load_model() first.")

#         # Drop target if present
#         X = input_df.copy()
#         if "growth_last_yr" in X.columns:
#             X = X.drop(columns=["growth_last_yr"])

#         # Predict
#         predictions = self.model.predict(X)

#         # Return in same scale as original (percent)
#         return predictions

#     def save_predictions(self, input_df: pd.DataFrame, predictions, output_path: Path):
#         """Save predictions combined with original data."""
#         output_path.parent.mkdir(parents=True, exist_ok=True)
#         results_df = input_df.copy()
#         results_df["predicted_growth_last_yr"] = predictions
#         results_df.to_csv(output_path, index=False)
#         logger.success(f"Predictions saved to {output_path}")


# if __name__ == "__main__":
#     logger.info("Starting Growth Predictor testing...")

#     predictor = GrowthPredictor()
#     predictor.load_model()

#     # --- TEST DATA ---
#     # Use a few rows from your processed CSV to ensure features match
#     TEST_CSV = PROCESSED_DATA_DIR / "growth_test.csv"
#     df_test = pd.read_csv(TEST_CSV)
#     df_test.columns = df_test.columns.str.strip()
#     logger.info(f"Loaded test data with shape: {df_test.shape}")

#     # Make predictions
#     predictions = predictor.predict(df_test)
#     logger.info(f"Predicted growth (%):\n{predictions}")

#     # Save predictions
#     OUTPUT_PATH = REPORTS_DIR / "predictions" / "growth_predictions.csv"
#     predictor.save_predictions(df_test, predictions, OUTPUT_PATH)
#     logger.info("Testing complete.")

import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
import joblib
from pathlib import Path
from loguru import logger
from inua360_the_kenyan_sme_ai_agent.config import MODELS_DIR, REPORTS_DIR

# --- Example raw data ---
raw_data = pd.DataFrame([
    {
        "company_id": 1,
        "country": "Ghana",
        "sector": "Education",
        "employees": 130,
        "annual_revenue": 386441,
        "tech_adoption_level": "Low",
        "main_challenges": "Awareness",
        "digital_tools_used": "CRM, WhatsApp, E-commerce",
        "funding_status": "Seed",
        "female_owned": "No",
        "remote_work_policy": "None",
        "growth_last_yr": 11
    },
    {
        "company_id": 2,
        "country": "Rwanda",
        "sector": "Farming",
        "employees": 367,
        "annual_revenue": 383576,
        "tech_adoption_level": "Low",
        "main_challenges": "Internet",
        "digital_tools_used": "WhatsApp",
        "funding_status": "Series A",
        "female_owned": "Yes",
        "remote_work_policy": "Partial",
        "growth_last_yr": 27
    },
    # add 3 more rows similarly
])

logger.info("Raw test data:")
logger.info(raw_data)

# --- Encoding & scaling (must match training) ---
categorical_cols = [
    "country", "sector", "tech_adoption_level",
    "main_challenges", "digital_tools_used",
    "funding_status", "female_owned", "remote_work_policy"
]

# Load the label encoders saved during training
label_encoders = joblib.load(MODELS_DIR / "label_encoders.pkl")

for col in categorical_cols:
    raw_data[col] = label_encoders[col].transform(raw_data[col].astype(str))

# Scale numeric columns
numeric_cols = [
    "company_id", "employees", "annual_revenue"
]
scaler = joblib.load(MODELS_DIR / "scaler.pkl")
raw_data[numeric_cols] = scaler.transform(raw_data[numeric_cols])

# --- Predict ---
model = joblib.load(MODELS_DIR / "growth_model.pkl")
X = raw_data.drop(columns=["growth_last_yr"])
raw_data["predicted_growth_last_yr"] = model.predict(X)

logger.info("Predictions with readable categorical values:")
logger.info(raw_data)
