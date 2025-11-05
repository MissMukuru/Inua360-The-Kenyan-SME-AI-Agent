from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from loguru import logger
from tqdm import tqdm
import typer

from inua360_the_kenyan_sme_ai_agent.config import FIGURES_DIR, PROCESSED_DATA_DIR, REPORTS_DIR

app = typer.Typer()

@app.command()
def main(
    input_path: Path = PROCESSED_DATA_DIR / "clean_data.csv",
):
    """
    Generate and save EDA plots for the African SME dataset.
    """
    logger.info(f"Loading data from {input_path}...")
    df = pd.read_csv(input_path)
    df.columns = df.columns.str.strip().str.lower()
    logger.success(f"Data loaded with shape: {df.shape}")

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    logger.info("Generating distribution plots...")
    plt.figure(figsize=(15, 5))

    plt.subplot(1, 3, 1)
    sns.histplot(df['annual_revenue'], kde=True, color='skyblue')
    plt.title('Distribution of Annual Revenue')
    plt.xlabel('Annual Revenue')
    plt.ylabel('Frequency')

    plt.subplot(1, 3, 2)
    sns.boxplot(x=df['num_employees'], color='lightcoral')
    plt.title('Distribution of Employees')
    plt.xlabel('Employees')

    plt.subplot(1, 3, 3)
    sns.countplot(x=df['tech_adoption_level'], color='lightgreen')
    plt.title('Tech Adoption Level')
    plt.xlabel('Tech Adoption Level')
    plt.ylabel('Count')

    plt.tight_layout()
    plt.savefig(REPORTS_DIR / "eda_distributions.png", dpi=300)
    plt.close()
    logger.success("Saved basic distribution plots.")

    logger.info("Generating scatter plot (Revenue vs Employees)...")
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='annual_revenue', y='num_employees', data=df)
    plt.title('Annual Revenue vs Number of Employees')
    plt.xlabel('Annual Revenue')
    plt.ylabel('Number of Employees')
    plt.tight_layout()
    plt.savefig(REPORTS_DIR / "revenue_vs_employees.png", dpi=300)
    plt.close()
    logger.success("Saved scatter plot for revenue vs employees.")

    logger.info("Generating correlation heatmap...")
    numerical_cols = df.select_dtypes(include=np.number).columns
    corr = df[numerical_cols].corr()

    plt.figure(figsize=(12, 10))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Correlation Matrix of Numerical Variables')
    plt.tight_layout()
    plt.savefig(REPORTS_DIR / "correlation_heatmap.png", dpi=300)
    plt.close()
    logger.success("Saved correlation heatmap.")

    logger.info("Generating country and sector distribution plots...")
    plt.figure(figsize=(12, 6))
    sns.countplot(y='country', data=df, order=df['country'].value_counts().index)
    plt.title('Companies by Country')
    plt.tight_layout()
    plt.savefig(REPORTS_DIR / "country_distribution.png", dpi=300)
    plt.close()

    plt.figure(figsize=(15, 8))
    sns.countplot(y='sector', data=df, order=df['sector'].value_counts().index)
    plt.title('Companies by Sector')
    plt.tight_layout()
    plt.savefig(REPORTS_DIR / "sector_distribution.png", dpi=300)
    plt.close()
    logger.success("Saved country and sector count plots.")

    if "funding_stage" in df.columns:
        plt.figure(figsize=(8, 6))
        sns.countplot(x='funding_stage', data=df)
        plt.title('Frequency of Funding Stage')
        plt.tight_layout()
        plt.savefig(REPORTS_DIR / "funding_stage_distribution.png", dpi=300)
        plt.close()
        logger.success("Saved funding stage count plot.")

    logger.info("Generating box and violin plots...")
    plt.figure(figsize=(15, 8))
    sns.boxplot(x='annual_revenue', y='sector', data=df)
    plt.title('Annual Revenue Distribution by Sector')
    plt.tight_layout()
    plt.savefig(REPORTS_DIR / "boxplot_revenue_sector.png", dpi=300)
    plt.close()

    plt.figure(figsize=(10, 6))
    sns.boxplot(x='funding_stage', y='annual_revenue', data=df)
    plt.title('Annual Revenue Distribution by Funding Stage')
    plt.tight_layout()
    plt.savefig(REPORTS_DIR / "boxplot_revenue_funding.png", dpi=300)
    plt.close()

    plt.figure(figsize=(15, 8))
    sns.violinplot(x='annual_revenue', y='sector', data=df)
    plt.title('Annual Revenue Distribution by Sector (Violin Plot)')
    plt.tight_layout()
    plt.savefig(REPORTS_DIR / "violin_revenue_sector.png", dpi=300)
    plt.close()

    plt.figure(figsize=(10, 6))
    sns.violinplot(x='funding_stage', y='annual_revenue', data=df)
    plt.title('Annual Revenue Distribution by Funding Stage (Violin Plot)')
    plt.tight_layout()
    plt.savefig(REPORTS_DIR / "violin_revenue_funding.png", dpi=300)
    plt.close()
    logger.success("Saved box and violin plots.")

    if {"female_owned", "revenue_growth_rate"}.issubset(df.columns):
        plt.figure(figsize=(8, 6))
        sns.boxplot(x='female_owned', y='revenue_growth_rate', data=df)
        plt.title("Female-Owned vs Revenue Growth Rate")
        plt.xlabel("Female-Owned")
        plt.ylabel("Revenue Growth Rate")
        plt.tight_layout()
        plt.savefig(REPORTS_DIR / "female_owned_vs_growth.png", dpi=300)
        plt.close()
        logger.success("Saved Female-Owned vs Growth plot.")

    logger.success(" All EDA visualizations generated and saved successfully.")


if __name__ == "__main__":
    app()
