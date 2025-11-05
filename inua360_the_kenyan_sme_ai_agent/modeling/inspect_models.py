import joblib
from pathlib import Path

MODEL_DIR = Path("models")  # change if your models are stored somewhere else

model_files = [
    "best_funding_model.pkl",
    "growth_model.pkl",
    "best_compliance_risk_level_model.pkl"
]

for model_name in model_files:
    model_path = MODEL_DIR / model_name
    print(f"\n=== Inspecting {model_name} ===")

    if not model_path.exists():
        print("⚠️  File not found")
        continue

    model = joblib.load(model_path)
    print("✅ Loaded:", type(model))

    # Check if it's a pipeline
    try:
        print("Feature count:", len(model.feature_names_in_))
        print("First 5 feature names:", list(model.feature_names_in_)[:5])
    except:
        print("❌ No feature_names_in_ attribute (likely not a pipeline)")
