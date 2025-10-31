from pathlib import Path
from sklearn.preprocessing import StandardScaler
from loguru import logger
import typer
import pandas as pd
import numpy as np

from inua360_the_kenyan_sme_ai_agent.config import EXTERNAL_DATA_DIR, PROCESSED_DATA_DIR

app = typer.Typer()


def compliance_risk(row):
    if row['num_employees'] < 10 and row["tech_adoption_level"] in ["Low", "None"]:
        return "High"
    elif 10 <= row["num_employees"] <= 50:
        return "Medium"
    else:
        return "Low"


@app.command()
def main(
    input_path: Path = EXTERNAL_DATA_DIR / "african_sme_dataset.csv",
    output_path: Path = PROCESSED_DATA_DIR / "training.csv",
):
    # Load data
    data = pd.read_csv(input_path)
    data.columns = data.columns.str.strip()
    data = data.drop(columns=['company_id'], errors='ignore')
    logger.info(f'Loaded dataset from {input_path}')

    # Feature engineering
    data['profit_margin'] = (data['annual_profit'] / data['annual_revenue']).replace([np.inf, -np.inf], 0).fillna(0)
    data['expense_ratio'] = (data['expenses_total'] / data['annual_revenue']).replace([np.inf, -np.inf], 0).fillna(0)
    data['employee_efficiency'] = data['annual_profit'] / (data['num_employees'] + 1)
    data['financial_health_index'] = (
        data['cashflow_stability_score'] + (1 - data['debt_ratio']) + data['credit_access']
    ) / 3
    data['compliance_score'] = (
        data['audit_score'] + data['environmental_compliance'] +
        data['data_protection_compliance'] + data['tax_compliance_status']
    ) / 4
    data['market_resilience'] = (
        data['country_gdp_growth'] + data['sector_avg_growth'] -
        data['inflation_rate'] + data['ease_of_doing_business_rank']
    ) / 4

    # Targets
    targets = ['funding_stage', 'revenue_growth_rate', 'tax_compliance_status', 'compliance_score']
    targets_df = data[targets].copy()

    # Features
    data_features = data.drop(columns=targets, errors='ignore')

    # Convert boolean columns to int
    bool_cols = ['female_owned','credit_access','online_presence','ecommerce_usage',
                 'cloud_services_used','cybersecurity_measures','tax_compliance_status',
                 'business_license_validity','environmental_compliance','data_protection_compliance']
    for col in bool_cols:
        if col in data_features.columns:
            data_features[col] = data_features[col].astype(int)

    # Encode categorical features
    categorical_cols = data_features.select_dtypes(include='object').columns
    data_features = pd.get_dummies(data_features, columns=categorical_cols, drop_first=True)
    logger.info("Categorical features encoded")

    # Standardize numeric features
    # Standardize numeric features with log transformation
    numeric_cols_to_scale = [
        'years_in_operation', 'annual_revenue', 'annual_profit', 'expenses_total',
        'num_employees', 'employee_growth_rate', 'avg_employee_salary',
        'training_investment_per_employee', 'digital_spending_ratio',
        'social_media_activity_score', 'customer_growth_rate',
        'customer_retention_rate', 'competition_intensity',
        'average_customer_ticket_size', 'profit_margin', 'expense_ratio',
        'employee_efficiency', 'financial_health_index',
        'compliance_score', 'market_resilience'
    ]
    numeric_cols_to_scale = [col for col in numeric_cols_to_scale if col in data_features.columns]

    # Apply log transform to reduce effect of extreme values
    data_features[numeric_cols_to_scale] = data_features[numeric_cols_to_scale].apply(
        lambda col: np.log1p(col - col.min() + 1)
    )

    # Standardize after log transform
    scaler = StandardScaler()
    data_features[numeric_cols_to_scale] = scaler.fit_transform(data_features[numeric_cols_to_scale])
    logger.info("Numeric features log-transformed and standardized")


    # Reattach targets
    data_final = pd.concat([data_features, targets_df], axis=1)

    # Save processed dataset
    data_final.to_csv(output_path, index=False)
    logger.success(f"Processed dataset saved at {output_path}")


if __name__ == "__main__":
    app()
