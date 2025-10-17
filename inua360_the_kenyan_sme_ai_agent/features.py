from pathlib import Path
from sklearn.preprocessing import StandardScaler, LabelEncoder
from loguru import logger
from tqdm import tqdm
import typer
import pandas as pd
import numpy as np

from inua360_the_kenyan_sme_ai_agent.config import PROCESSED_DATA_DIR

app = typer.Typer()


def compliance_risk(row):
    if row['employees'] < 10 and row["tech_adoption_level"] in ["Low", "None"]:
        return "High"
    elif 10 <= row["employees"] <= 50:
        return "Medium"
    else:
        return "Low"


@app.command()
def main(
    input_path: Path = PROCESSED_DATA_DIR / "Clean_dat.csv",
    output_path: Path = PROCESSED_DATA_DIR / "funding_train.csv",
):
    # Load data
    data = pd.read_csv(input_path)
    logger.info(f'Loaded dataset from {input_path}')

    data.columns = data.columns.str.strip()

    # Create new feature: revenue per employee
    logger.info("Creating new features...")
    data['revenue_per_employee'] = data['annual_revenue'] / data['employees']
    data['revenue_per_employee'].replace([np.inf, -np.inf], np.nan, inplace=True)

    # Create compliance risk target
    logger.info("Creating the Compliance_risk feature...")
    data['Compliance_risk'] = data.apply(compliance_risk, axis=1)

    # Ensure funding_status column exists (simulate if missing)
    if 'funding_status' not in data.columns:
        logger.warning("'funding_status' column missing — generating synthetic targets for now.")
        data['funding_status'] = (
            0.4 * data['annual_revenue'] +
            0.3 * data['employees'] +
            0.2 * data['revenue_per_employee'] +
            np.random.normal(0, 0.05, len(data))
        )

    # Encode categorical columns
    logger.info("Encoding categorical features...")
    categorical_cols = data.select_dtypes(include='object').columns
    for col in tqdm(categorical_cols, desc='Encoding categorical columns'):
        le = LabelEncoder()
        data[col] = le.fit_transform(data[col].astype(str))

    # Standardize numerical columns
    logger.info("Scaling numerical features...")
    numerical_features = data.select_dtypes(include=['int64', 'float64']).columns
    scaler = StandardScaler()
    for col in tqdm(numerical_features, desc='Scaling numerical columns'):
        data[col] = scaler.fit_transform(data[[col]])

    # Save processed data
    data.to_csv(output_path, index=False)
    logger.success(f"Processed dataset saved to {output_path}")


if __name__ == "__main__":
    app()
