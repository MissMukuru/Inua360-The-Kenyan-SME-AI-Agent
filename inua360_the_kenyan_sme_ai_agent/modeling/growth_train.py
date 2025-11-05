from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
import pandas as pd
import joblib
import lightgbm as lgb

# 1️⃣ Prepare X and y
X = df.drop(columns=["revenue_growth_rate"])
y = df["revenue_growth_rate"]

categorical_cols = X.select_dtypes(include=["object"]).columns.tolist()
numeric_cols = X.select_dtypes(include=["int64","float64"]).columns.tolist()

# 2️⃣ Fit encoders/scalers separately
ohe = OneHotEncoder(handle_unknown="ignore", sparse=False)
X_cat = ohe.fit_transform(X[categorical_cols])

scaler = StandardScaler()
X_num = scaler.fit_transform(X[numeric_cols])

# 3️⃣ Combine numeric + categorical manually
import numpy as np
X_processed = np.hstack([X_num, X_cat])

# 4️⃣ Train model
model = lgb.LGBMRegressor(n_estimators=500, learning_rate=0.01)
model.fit(X_processed, y)

# 5️⃣ Save everything
joblib.dump(model, "growth_model.pkl")
joblib.dump(ohe, "growth_ohe.pkl")
joblib.dump(scaler, "growth_scaler.pkl")
joblib.dump(list(numeric_cols + list(ohe.get_feature_names_out())), "growth_features.pkl")
