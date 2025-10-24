from pathlib import Path
from sklearn.preprocessing import StandardScaler, LabelEncoder
from loguru import logger
from tqdm import tqdm
import typer
import pandas as pd
import numpy as np

from inua360_the_kenyan_sme_ai_agent.config import PROCESSED_DATA_DIR, INTERIM_DATA_DIR

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
    input_path: Path = INTERIM_DATA_DIR / "Clean_data.csv",
    output_path: Path = PROCESSED_DATA_DIR / "funding_train.csv",
):
    # Load data
    data = pd.read_csv(input_path)
    data.columns=data.columns.str.strip()
    logger.info(f'Loaded dataset from {input_path}')

    data.columns = data.columns.str.strip()

    # Create new feature: revenue per employee
    logger.info("Creating new features...")
    data['revenue_per_employee'] = data['annual_revenue'] / data['employees']
    data['revenue_per_employee'].replace([np.inf, -np.inf], np.nan, inplace=True)

    # Create compliance risk target
    logger.info("Creating the Compliance_risk feature...")
    data['Compliance_risk'] = data.apply(compliance_risk, axis=1)


    # Encode categorical columns
    logger.info("Encoding categorical features...")
    categorical_cols=data.select_dtypes(include='object')
    categorical_cols.columns.to_list()
    label_encoders = {}

    for col in categorical_cols:
        le = LabelEncoder()
        data[col]=le.fit_transform(data[col].astype(str))
        label_encoders[col] = le

    data.nunique()

    funding_status=data['funding_status']

    data=data.drop('funding_status', axis=1)

    data.head()

    # Standardize numerical columns
    logger.info("Scaling numerical features...")
    numerical_features = data.select_dtypes(include=['int64', 'float64']).columns
    scaler = StandardScaler()

    for col in numerical_features:
        data[numerical_features]=scaler.fit_transform(data[numerical_features])

    data['funding_status'] = funding_status


    # Save processed data
    data.to_csv(output_path, index=False)
    logger.success(f"The final dataset for modelling \n {data.head()}")


if __name__ == "__main__":
    app()
