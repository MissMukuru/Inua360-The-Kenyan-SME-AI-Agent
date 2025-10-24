import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier
from loguru import logger
import typer

from inua360_the_kenyan_sme_ai_agent.config import MODELS_DIR, PROCESSED_DATA_DIR, INTERIM_DATA_DIR

app = typer.Typer()


@app.command()
def main(
    funding_growth_path: Path = MODELS_DIR/ "Best_model",
    input_path: Path = INTERIM_DATA_DIR/"funding_train.csv"

):
    logger.info('Loading the dataset and splitting into training and test_sets')
    data = pd.read_csv(input_path)
    data.columns=data.columns.str.strip()
    X = data.drop(columns=["funding_status"])
    y = data["funding_status"]

    Xf_train,Xf_test,yf_train, yf_test = train_test_split(X,y, test_size=0.2, random_state=42)

    logger.info("Modelling the Logistic Regression Classifier")
    param_grid_log = {
        "C": [0.01, 0.1, 1, 10],
        "solver": ["lbfgs", "saga"],
        "penalty": ["l2"]
    }
    grid_search_log = GridSearchCV(
        LogisticRegression(max_iter=5000),
        param_grid_log,
        cv=3,
        n_jobs=-1,
        scoring="accuracy"
    )
    grid_search_log.fit(Xf_train, yf_train)

    logger.info("Moving onto modelling the GradientBoostingRegressor")
    param_grid_grad = {
        'n_estimators': [100, 200, 300],
        'learning_rate': [0.01, 0.05, 0.1],
        'max_depth': [3, 5, 7],
        'subsample': [0.8, 1.0]
    }
    grid_search_grad = GridSearchCV(
        GradientBoostingClassifier(random_state=42),
        param_grid_grad,
        cv = 3,
        scoring = 'r2',
        n_jobs=-1
    )
    grid_search_grad.fit(Xf_train, yf_train)

    logger.info('Modelling the RandomForestRegressor')
    param_grid_rand={
        'n_estimators': [100, 200, 300],
        'max_depth': [5, 10, 15, None],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'max_features': ['sqrt', 'log2']
    }

    grid_search_rand=GridSearchCV(
        estimator=rf,
        param_grid=param_grid_rand,
        cv=3,
        n_jobs=-1,
        verbose=2,
        scoring="r2"
    )
    grid_search_rand.fit(Xf_train,yf_train)

    logger.info("Modelling the decision tree")
    param_grid_tree = {
        'criterion': ['gini', 'entropy'],
        'max_depth': ['5, 10, 20, None'],
        'min_samples_split': [2,5, 10]
    }
    grid_search_tree=GridSearchCV(
        DecisionTreeClassifier(random_state=42),
        param_grid=param_grid_tree,
        cv=3,
        n_jobs=-1,
        scoring='accuracy'
    )

    logger.info("Modelling the XGBoost Classifier")
    param_grid_xgb = {
        "n_estimators": [100, 200],
        "learning_rate": [0.01, 0.05, 0.1],
        "max_depth": [3, 5, 7],
        "subsample": [0.8, 1.0],
        "colsample_bytree": [0.8, 1.0]
    }
    grid_search_xgb = GridSearchCV(
        XGBClassifier(use_label_encoder=False, eval_metric="mlogloss", random_state=42),
        param_grid_xgb,
        cv=3,
        n_jobs=-1,
        scoring="accuracy"
    )
    grid_search_xgb.fit(Xf_train, yf_train)

    logger.info("Modelling the Support Vector Classifier")
    param_grid_svm = {
        "C": [0.1, 1, 10],
        "kernel": ["linear", "rbf", "poly"],
        "gamma": ["scale", "auto"]
    }
    grid_search_svm = GridSearchCV(
        SVC(probability=True),
        param_grid_svm,
        cv=3,
        n_jobs=-1,
        scoring="accuracy"
    )
    grid_search_svm.fit(Xf_train, yf_train)

    models = {
        "Logistic Regression": grid_search_log,
        "Decision Tree": grid_search_tree,
        "SVM": grid_search_svm,
        "Gradient Boosting": grid_search_grad,
        "Random Forest": grid_search_rand,
        "XGBoost": grid_search_xgb
    }

    best_model_name=None
    best_model = None
    best_score = 0

    for name, grid in models.items():
        y_pred=grid.best_estimator_.predict(Xf_test)
        acc=accuracy_score(yf_test,y_pred)
        logger.info(f"{name} Accuracy: {acc:.4f}")
        if acc > best_score:
            best_score=acc
            best_model_name=name
            best_model=grid.best_estimator_

    logger.success(f"Best_ model: {best_model_name} with an accuracy of {best_score:.4f}")
    logger.info("Classification report")

    joblib.dump(best_model, funding_growth_path)
    logger.success(f"Model saved to {funding_growth_path}")

if __name__ == "__main__":
    app()
