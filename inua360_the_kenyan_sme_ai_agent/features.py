from pathlib import Path
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
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
    input_path: Path = PROCESSED_DATA_DIR / "Sales.csv",
    labels_path: Path = PROCESSED_DATA_DIR / "labels.csv",
    output_path: Path = PROCESSED_DATA_DIR / "features.csv",
):
    data = pd.read_csv(input_path)
    logger.info(f'Loading dataset from {input_path}')

    data.columns = data.columns.str.strip()

    logger.info("Creating new features")
    data['revenue_per_employee'] = data['annual_revenue'] / data['employees']
    data['revenue_per_employee'].replace([np.inf, -np.inf], np.nan, inplace=True)

    logger.info("Creating the target feature")
    data['Compliance_risk'] = data.apply(compliance_risk, axis=1)

    logger.info('Encoding Categorical features...')
    categorical_cols = data.select_dtypes(include='object').columns
    label_encoders = {}

    for col in tqdm(categorical_cols, desc='Encoding categorical Columns'):
        le = LabelEncoder()
        data[col] = le.fit_transform(data[col].astype(str))
        label_encoders[col] = le

    logger.info("Standardizing the numerical features")
    numerical_features = data.select_dtypes(include=['int64', 'float64']).columns
    scaler = StandardScaler()

    for col in tqdm(numerical_features, desc='Scaling numerical columns'):
        data[col] = scaler.fit_transform(data[[col]])

    logger.info("Splitting the dataset into train and test splits")
    X_growth = data.drop(columns=["growth_last_yr"])
    y_growth = data["growth_last_yr"]

    # Funding Model
    X_funding = data.drop(columns=["funding_status"])
    y_funding = data["funding_status"]

    # Compliance Risk Model
    X_risk = data.drop(columns=["Compliance_risk"])
    y_risk = data["Compliance_risk"]

    for name, X, y in [
        ('growth', X_growth, y_growth),
        ('funding', X_funding, y_funding),
        ('risk', X_risk, y_risk)
    ]:
        logger.info(f'Creating train test split for {name} model....')
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        X_train.to_csv(output_path.parent / f"{name}_train.csv", index=False)
        X_test.to_csv(output_path.parent / f"{name}_test.csv", index=False)
        y_train.to_csv(output_path.parent / f"{name}_y_train.csv", index=False)
        y_test.to_csv(output_path.parent / f"{name}_y_test.csv", index=False)

        logger.success(f'{name.capitalize()} data saved to {output_path.parent}')

    logger.info(f'The processed data has been saved in: {output_path.parent}')


if __name__ == "__main__":
    app()
