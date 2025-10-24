from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from loguru import logger
from tqdm import tqdm
import typer

from inua360_the_kenyan_sme_ai_agent.config import FIGURES_DIR, PROCESSED_DATA_DIR, INTERIM_DATA_DIR, REPORTS_DIR, MODELS_DIR

app = typer.Typer()

logger.info(f"Prediction Figures will be saved to {FIGURES_DIR}")

logger.info("Starting plot generation...")
    

def plot_actual_vs_predicted(y_true, y_pred, filename = "actual_vs_predicted.png"):
    plt.figure(figsize=(8, 6))
    sns.scatter(x=y_true, y=y_pred)
    plt.plot([y_true.min(), y_true.max()], [y_true.min(), y_true.max()], 'r--')
    plt.xlabel('Actual Growth Last Year')
    plt.ylabel('Predicted Growth Last Year')
    plt.title('Actual vs Predicted Growth')
    plt.savefig(FIGURES_DIR / filename, dpi=300)
    plt.close()
    logger.success(f"Saved actual vs predicted plot to {FIGURES_DIR / filename}")
    
def plot_residuals(y_true, y_pred, filename="residuals.png"):
    residuals = y_true - y_pred
    plt.figure(figsize=(8, 6))
    sns.histplot(residuals, kde=True, color="salmon")
    plt.xlabel("Residuals (Actual - Predicted)")
    plt.ylabel("Frequency")
    plt.title("Residuals Distribution")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / filename, dpi=300)
    plt.close()
    logger.success(f"Saved Residuals plot to {FIGURES_DIR / filename}")


def plot_predicted_distribution(y_pred, filename="predicted_distribution.png"):
    plt.figure(figsize=(8, 6))
    sns.histplot(y_pred, kde=True, color="teal")
    plt.xlabel("Predicted Growth Last Year")
    plt.ylabel("Frequency")
    plt.title("Predicted Growth Distribution")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / filename, dpi=300)
    plt.close()
    logger.success(f"Saved Predicted Distribution plot to {FIGURES_DIR / filename}")


@app.command()
def main(
    input_path: Path = PROCESSED_DATA_DIR / "clean_data.csv",
  
):
    logger.info(f"Loading data from {input_path}...")
    df = pd.read_csv(input_path)
    df.columns = df.columns.str.strip()  
    logger.success(f"Data loaded with shape: {df.shape}")
    
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    
    logger.info("Starting plot generation...")
    
    logger.info("Generating numerical feature distributions...")
    num_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

    plt.figure(figsize=(14, 8))
    df[num_cols].hist(bins=20, figsize=(14, 8))
    plt.suptitle("Distribution of Numerical Features", fontsize=14)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "numerical_distributions.png", dpi=300)
    plt.close()
    logger.success("Saved numerical distributions.")

    logger.info("Generating correlation heatmap...")
    plt.figure(figsize=(10, 8))
    corr = df[num_cols].corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm")
    plt.title("Correlation Heatmap", fontsize=16)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "correlation_heatmap.png", dpi=300)
    plt.close()
    logger.success("Saved correlation heatmap.")
    
    
    if "funding_status" in df.columns:
        logger.info("Plotting funding status distribution...")
        plt.figure(figsize=(6, 5))
        sns.countplot(x="funding_status", data=df, palette="Set2")
        plt.title("Funding Status Distribution")
        plt.xlabel("Funding Status")
        plt.ylabel("Count")
        plt.tight_layout()
        plt.savefig(FIGURES_DIR / "funding_status_distribution.png", dpi=300)
        plt.close()
        logger.success("Saved funding status count plot.")

    if "growth_last_year" in df.columns:
        logger.info("Plotting growth last year distribution...")
        plt.figure(figsize=(7, 5))
        sns.histplot(df["growth_last_year"], bins=20, kde=True, color="teal")
        plt.title("Growth Last Year Distribution")
        plt.xlabel("Growth Last Year (%)")
        plt.tight_layout()
        plt.savefig(FIGURES_DIR / "growth_last_year_distribution.png", dpi=300)
        plt.close()
        logger.success("Saved growth distribution plot.")

    logger.info("Generating boxplots for numerical features...")
    for col in num_cols:
        plt.figure(figsize=(6, 4))
        sns.boxplot(x=df[col], color="orange")
        plt.title(f"Boxplot of {col}")
        plt.tight_layout()
        plt.savefig(FIGURES_DIR / f"boxplot_{col}.png", dpi=300)
        plt.close()
    logger.success("Saved boxplots for all numeric features.")


    if {"annual_revenue", "employees"}.issubset(df.columns):
        logger.info("Generating scatter plots...")
        plt.figure(figsize=(7, 5))
        sns.scatterplot(
            data=df,
            x="employees",
            y="annual_revenue",
            hue="funding_status" if "funding_status" in df.columns else None,
            palette="viridis",
        )
        plt.title("Employees vs Annual Revenue (colored by Funding Status)")
        plt.tight_layout()
        plt.savefig(FIGURES_DIR / "employees_vs_revenue.png", dpi=300)
        plt.close()
        logger.success("Saved scatter plot for employees vs revenue.")


    logger.info("Generating pairplot of selected numeric features...")
    selected_cols = num_cols[:5]  
    sns.pairplot(df[selected_cols])
    plt.suptitle("Pairplot of Selected Numerical Features", y=1.02)
    plt.savefig(FIGURES_DIR / "pairplot_numeric.png", dpi=300)
    plt.close()
    logger.success("Saved pairplot for numerical features.")

    logger.success("All EDA plots generated successfully.")


if __name__ == "__main__":
    app()

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # ---- REPLACE THIS WITH YOUR OWN CODE ----
    logger.info("Generating plot from data...")
    for i in tqdm(range(10), total=10):
        if i == 5:
            logger.info("Something happened for iteration 5.")
    logger.success("Plot generation complete.")
    # -----------------------------------------


if __name__ == "__main__":
    app()
