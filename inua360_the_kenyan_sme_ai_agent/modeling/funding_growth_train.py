import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier
from loguru import logger
import warnings
import typer

from inua360_the_kenyan_sme_ai_agent.config import MODELS_DIR, PROCESSED_DATA_DIR

app = typer.Typer()
warnings.filterwarnings("ignore")  # suppress convergence & deprecation warnings

@app.command()
def main(
    funding_model_path: Path = MODELS_DIR / "best_funding_model.pkl",
    funding_features_path: Path = MODELS_DIR / "funding_features.pkl",
    input_path: Path = PROCESSED_DATA_DIR / "training.csv"
):
    logger.info("Loading dataset...")
    data = pd.read_csv(input_path)
    data.columns = data.columns.str.strip()

    # Drop missing target rows
    data = data.dropna(subset=["funding_stage"])
    X = data.drop(columns=["funding_stage"])
    y = data["funding_stage"]

    # One-hot encode categorical features
    X = pd.get_dummies(X, drop_first=True)

    # Standardize numeric columns
    numeric_cols = X.select_dtypes(include=np.number).columns
    scaler = StandardScaler()
    X[numeric_cols] = scaler.fit_transform(X[numeric_cols])

    # Save the feature list for later use in prediction
    MODELS_DIR.mkdir(exist_ok=True, parents=True)
    joblib.dump(X.columns.tolist(), funding_features_path)
    logger.success(f"Funding feature list saved to {funding_features_path}")

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Define models and parameter grids
    models = {
        "Logistic Regression": (LogisticRegression(max_iter=5000), {
            "C": [0.1, 1],
            "solver": ["lbfgs"],
            "penalty": ["l2"]
        }),
        "Random Forest": (RandomForestClassifier(random_state=42), {
            "n_estimators": [100, 200],
            "max_depth": [5, 10],
            "min_samples_split": [2, 5],
            "min_samples_leaf": [1, 2]
        }),
        "Gradient Boosting": (GradientBoostingClassifier(random_state=42), {
            "n_estimators": [100, 200],
            "learning_rate": [0.05],
            "max_depth": [3, 5],
            "subsample": [1.0]
        }),
        "Decision Tree": (DecisionTreeClassifier(random_state=42), {
            "criterion": ["gini", "entropy"],
            "max_depth": [5, 10],
            "min_samples_split": [2, 5]
        }),
        "SVM": (SVC(probability=True), {
            "C": [1, 10],
            "kernel": ["linear", "rbf"],
            "gamma": ["scale"]
        })
    }

    best_model_name = None
    best_model = None
    best_score = 0

    # Train and evaluate each model
    for name, (model, params) in models.items():
        logger.info(f"Training {name}...")
        grid = GridSearchCV(model, params, cv=3, scoring="accuracy", n_jobs=2)
        grid.fit(X_train, y_train)

        y_pred = grid.best_estimator_.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        logger.info(f"{name} Accuracy: {acc:.4f}")

        if acc > best_score:
            best_score = acc
            best_model_name = name
            best_model = grid.best_estimator_

    logger.success(f"Best model: {best_model_name} with accuracy {best_score:.4f}")
    logger.info("\n" + classification_report(y_test, best_model.predict(X_test)))

    # Save the trained model
    joblib.dump(best_model, funding_model_path)
    logger.success(f"Model saved to {funding_model_path}")

if __name__ == "__main__":
    app()
