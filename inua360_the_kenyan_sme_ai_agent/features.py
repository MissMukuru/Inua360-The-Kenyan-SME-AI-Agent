from pathlib import Path
from sklearn.preprocessing import StandardScaler, LabelEncoder
from loguru import logger
from tqdm import tqdm
import typer
import pandas as pd
import numpy as np

from inua360_the_kenyan_sme_ai_agent.config import PROCESSED_DATA_DIR,INTERIM_DATA_DIR

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
    input_path: Path = PROCESSED_DATA_DIR / "Clean_data.csv",
    output_path: Path = INTERIM_DATA_DIR / "funding_train.csv",
):
    # Load data
    data = pd.read_csv(input_path)
    logger.info(f'Loaded dataset from {input_path}')

    data.columns = data.columns.str.strip()

    # Create new feature: revenue per employee
    logger.info("Creating new features...")
    data['revenue_per_employee'] = data['annual_revenue'] / data['employees']
    data['revenue_per_employee'].replace([np.inf, -np.inf], np.nan)


   
if __name__ == "__main__":
    app()
