# generate_sme_dataset.py
# Generates a realistic but learnable SME dataset for training:
# - training.csv (10,000 rows) saved to PROCESSED_DATA_DIR
# - includes targets: funding_stage, compliance_risk_level, revenue_growth_rate

import numpy as np
import pandas as pd
import random
from pathlib import Path
from loguru import logger
import typer

from inua360_the_kenyan_sme_ai_agent.config import PROCESSED_DATA_DIR

app = typer.Typer()
random.seed(42)
np.random.seed(42)


def _map_to_funding_stage(score):
    """
    Score roughly in [-1, 1]. We'll map to funding classes with a realistic skew.
    Distribution intention (approx):
    None ~ 40%, Grant ~ 12%, Angel ~ 10%, Seed ~ 18%, Series A ~ 12%, Series B ~ 6%, Debt ~ 2%
    """
    # add some noise
    s = score + np.random.normal(0, 0.15, size=score.shape)
    stages = []
    for v in s:
        if v < -0.25:
            stages.append("None")
        elif v < -0.0:
            stages.append("Grant")
        elif v < 0.1:
            stages.append("Angel")
        elif v < 0.35:
            stages.append("Seed")
        elif v < 0.6:
            stages.append("Series A")
        elif v < 0.8:
            stages.append("Series B")
        else:
            stages.append("Debt Financing")
    return stages


def _map_to_compliance_level(score):
    """
    Score in [0,1] higher => more compliant (lower risk).
    We invert so low score => high risk.
    Distribution intention:
    Low  ~ 20%, Moderate ~ 50%, High ~ 20%, Critical ~ 10%
    """
    s = score + np.random.normal(0, 0.08, size=score.shape)
    levels = []
    for v in s:
        if v >= 0.8:
            levels.append("Low")
        elif v >= 0.5:
            levels.append("Moderate")
        elif v >= 0.25:
            levels.append("High")
        else:
            levels.append("Critical")
    return levels


@app.command()
def main(
    n_samples: int = 10000,
    output_path: Path = PROCESSED_DATA_DIR / "african_sme_dataset.csv"
):
    logger.info(f"Generating synthetic SME dataset with {n_samples} rows...")

    # Basic numeric & categorical distributions
    num_employees = np.random.randint(1, 500, n_samples)
    annual_revenue = np.round(np.random.lognormal(mean=10.5, sigma=1.2, size=n_samples)).astype(int)  # wide spread
    avg_employee_salary = np.round(np.random.uniform(300, 8000, size=n_samples), 2)
    expenses_total = np.round(annual_revenue * np.random.uniform(0.4, 0.95, size=n_samples), 2)
    customer_growth_rate = np.round(np.random.uniform(-0.2, 0.6, size=n_samples), 3)
    customer_retention_rate = np.round(np.random.beta(2, 3, size=n_samples), 3)  # skewed towards lower retention
    digital_spending_ratio = np.round(np.random.beta(1.5, 5, size=n_samples), 3)  # many low spenders
    years_in_operation = np.random.randint(0, 30, n_samples)
    profit_to_expense_ratio = np.round(np.random.beta(2, 4, size=n_samples), 3)

    regions = ["Urban", "Rural"]
    sectors = ["Tech", "Finance", "Healthcare", "Retail", "Manufacturing", "Education", "Agriculture"]
    tech_levels = ["Low", "Medium", "High"]
    remote_policies = ["None", "Partial", "Full"]

    region = np.random.choice(regions, size=n_samples, p=[0.7, 0.3])
    sector = np.random.choice(sectors, size=n_samples)
    tech_adoption_level = np.random.choice(tech_levels, size=n_samples, p=[0.45, 0.35, 0.2])
    remote_work_policy = np.random.choice(remote_policies, size=n_samples, p=[0.6, 0.3, 0.1])

    # Funding model features
    has_pitch_deck = np.random.choice([0, 1], size=n_samples, p=[0.7, 0.3])
    # cash flow score correlated with profit_to_expense_ratio and revenue stability
    revenue_stability = 1 - np.abs(np.random.normal(loc=0, scale=0.25, size=n_samples))  # centered around 1 but with noise
    cash_flow_score = np.clip(0.6 * profit_to_expense_ratio + 0.4 * revenue_stability, 0, 1)
    credit_score = np.clip(np.random.beta(2.5, 2.5, size=n_samples) * 0.8 + (cash_flow_score * 0.2), 0, 1)
    registered_business = np.random.choice([0, 1], size=n_samples, p=[0.15, 0.85])
    prior_investment = np.random.choice(["None", "Angels", "VC", "Gov Grant"], size=n_samples, p=[0.6, 0.15, 0.08, 0.17])
    traction_score = np.clip(0.5 * (customer_growth_rate - customer_growth_rate.min()) / (customer_growth_rate.max() - customer_growth_rate.min()) + 
                             0.5 * (annual_revenue / (annual_revenue.max() + 1)), 0, 1)
    female_owned = np.random.choice([0, 1], size=n_samples, p=[0.75, 0.25])

    # Compliance features
    # tax compliance: more likely if registered_business and good bookkeeping proxy
    bookkeeping_quality = np.clip(np.random.beta(2, 3, size=n_samples) + 0.3 * cash_flow_score, 0, 1)
    tax_compliance_status = np.where(
        bookkeeping_quality + 0.25 * registered_business + np.random.normal(0, 0.1, n_samples) > 0.6,
        "Compliant",
        np.where(bookkeeping_quality > 0.35, "Late Filing", "Not Registered")
    )
    regulatory_license_status = np.random.choice(["Valid", "Expired", "Missing"], size=n_samples, p=[0.75, 0.15, 0.10])
    data_protection_score = np.clip(0.2 * tech_adoption_level.tolist().__len__() + np.random.beta(1.5, 3.0, size=n_samples), 0, 1)
    # make data_protection_score somewhat correlated with tech adoption and digital_spending_ratio
    data_protection_score = np.clip(0.25 * (np.array([{"Low": 0, "Medium": 0.5, "High": 1}[t] for t in tech_adoption_level])) + 
                                     0.5 * digital_spending_ratio + np.random.normal(0, 0.12, n_samples), 0, 1)
    employee_contracts_verified = np.where((num_employees < 5) & (np.random.rand(n_samples) > 0.5), 0, np.random.choice([0, 1], size=n_samples, p=[0.25, 0.75]))
    AML_risk_flag = np.random.choice([0, 1], size=n_samples, p=[0.9, 0.1])
    financial_transparency_score = np.clip(0.4 * bookkeeping_quality + 0.4 * cash_flow_score + np.random.normal(0, 0.15, n_samples), 0, 1)

    # Compliance risk aggregated score (higher => better compliance)
    compliance_score = np.clip(0.35 * financial_transparency_score + 0.25 * (bookkeeping_quality) + 0.2 * data_protection_score + 0.1 * registered_business + 0.1 * (1 - AML_risk_flag), 0, 1)
    compliance_risk_level = _map_to_compliance_level(compliance_score)

    # revenue_growth_rate (target, keep correlated with features similar to prior snippet but improved)
    noise = np.random.normal(0, 0.05, n_samples)
    revenue_growth_rate = (
        0.0007 * num_employees +
        0.28 * digital_spending_ratio +
        0.25 * np.clip(customer_growth_rate, -0.2, 0.6) +
        0.18 * profit_to_expense_ratio +
        0.12 * traction_score +
        noise
    )
    revenue_growth_rate = np.clip(revenue_growth_rate, -0.3, 1.2)  # allow some high growth outliers

    # Funding stage mapped from a composite funding score
    # Funding score combines traction, credit, cash flow, registration, and prior investment
    prior_inv_score = np.array([{"None": 0.0, "Angels": 0.4, "VC": 0.8, "Gov Grant": 0.3}[x] for x in prior_investment])
    funding_score = np.clip(0.35 * traction_score + 0.25 * credit_score + 0.2 * cash_flow_score + 0.15 * registered_business + 0.05 * prior_inv_score, -1, 1)
    funding_stage = _map_to_funding_stage(funding_score)

    # Build DataFrame
    df = pd.DataFrame({
        "company_id": np.arange(1, n_samples + 1),
        "region": region,
        "sector": sector,
        "num_employees": num_employees,
        "annual_revenue": annual_revenue,
        "avg_employee_salary": avg_employee_salary,
        "expenses_total": expenses_total,
        "customer_growth_rate": customer_growth_rate,
        "customer_retention_rate": customer_retention_rate,
        "digital_spending_ratio": digital_spending_ratio,
        "years_in_operation": years_in_operation,
        "profit_to_expense_ratio": profit_to_expense_ratio,
        "tech_adoption_level": tech_adoption_level,
        "remote_work_policy": remote_work_policy,
        # funding features
        "has_pitch_deck": has_pitch_deck,
        "cash_flow_score": np.round(cash_flow_score, 3),
        "credit_score": np.round(credit_score, 3),
        "registered_business": registered_business,
        "prior_investment": prior_investment,
        "traction_score": np.round(traction_score, 3),
        "female_owned": female_owned,
        # compliance features
        "bookkeeping_quality": np.round(bookkeeping_quality, 3),
        "tax_compliance_status": tax_compliance_status,
        "regulatory_license_status": regulatory_license_status,
        "data_protection_score": np.round(data_protection_score, 3),
        "employee_contracts_verified": employee_contracts_verified,
        "AML_risk_flag": AML_risk_flag,
        "financial_transparency_score": np.round(financial_transparency_score, 3),
        # targets
        "compliance_risk_level": compliance_risk_level,
        "funding_stage": funding_stage,
        "revenue_growth_rate": np.round(revenue_growth_rate, 4)
    })

    # Ensure path exists and save
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.success(f"Saved training dataset with targets to: {output_path}")


if __name__ == "__main__":
    app()
