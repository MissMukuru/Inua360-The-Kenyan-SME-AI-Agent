# 🎯 How to Run Inua360 Dashboard

## 🚀 Fastest Way to Start

### Windows Users:
```bash
start_dashboard.bat
```
Select option **2** (Run both API + Dashboard)

### Mac/Linux/Python Users:
```bash
python start.py
```
Select option **2** (Run both API + Dashboard)

---

## 📋 What Happens When You Run It?

1. ✅ Checks if `.env` exists (creates template if not)
2. ✅ Checks if `.streamlit/secrets.toml` exists (creates template if not)
3. ✅ Starts FastAPI server on `http://localhost:8000`
4. ✅ Starts Streamlit dashboard on `http://localhost:8501`
5. ✅ Opens browser automatically

---

## 🔑 Required Setup (One Time Only)

### 1. Add OpenAI API Key

Edit `.env` file:
```env
OPENAI_API_KEY=sk-proj-your-actual-key-here
PORT=8000
```

### 2. Configure Dashboard Secrets (Optional)

Edit `.streamlit/secrets.toml`:
```toml
API_BASE_URL = "http://localhost:8000"
N8N_WEBHOOK_URL = "https://abby218.app.n8n.cloud/webhook/sme-data"
SLACK_WEBHOOK_URL = "your_actual_slack_webhook_url"
ELEVENLABS_API_KEY = "your_actual_elevenlabs_key"
```

> **Note:** Dashboard works without Slack/ElevenLabs keys (those features just won't work)

---

## 📍 Accessing the Application

### Dashboard UI:
```
http://localhost:8501
```

### API Documentation:
```
http://localhost:8000/docs
```

---

## 🎨 Understanding the API Endpoints

The `predictions_api.py` file exposes these endpoints:

| Endpoint | What It Does | Used By |
|----------|--------------|---------|
| `/predict/funding` | Predicts funding readiness score | Individual model testing |
| `/predict/compliance` | Predicts compliance risk level | Individual model testing |
| `/predict/growth` | Predicts revenue growth percentage | Individual model testing |
| `/predict/sme` | **All predictions + AI advice** | **Dashboard uses this!** |

The dashboard calls `/predict/sme` which:
1. Runs all 3 models (funding, compliance, growth)
2. Generates AI advice using GPT-4
3. Sends data to n8n webhook (automation)
4. Returns combined results

---

## 🧪 Testing Without the Dashboard

### Option 1: Use API Docs (Easiest)
1. Start API: `python inua360_the_kenyan_sme_ai_agent\modeling\predictions_api.py`
2. Open browser: `http://localhost:8000/docs`
3. Click `POST /predict/sme`
4. Click "Try it out"
5. Use sample JSON from `test_sme_data.json`
6. Click "Execute"

### Option 2: Use curl
```bash
curl -X POST "http://localhost:8000/predict/sme" ^
  -H "Content-Type: application/json" ^
  -d @test_sme_data.json
```

### Option 3: Use Python
```python
import requests

response = requests.post(
    "http://localhost:8000/predict/sme",
    json={
        "annual_revenue": 5000000,
        "expenses_total": 3000000,
        # ... other fields from test_sme_data.json
    }
)
print(response.json())
```

---

## 🎯 Complete Workflow

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  User fills form in Dashboard (app.py)                  │
│  http://localhost:8501                                  │
│                                                         │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ Sends SME data via HTTP POST
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  API receives data (predictions_api.py)                 │
│  http://localhost:8000/predict/sme                      │
│                                                         │
│  1. Preprocesses data                                   │
│  2. Runs 3 ML models (funding, compliance, growth)      │
│  3. Calls OpenAI GPT-4 for advice                       │
│  4. Sends data to n8n webhook (background)              │
│  5. Returns JSON response                               │
│                                                         │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ Returns predictions + AI advice
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  Dashboard displays results (app.py)                    │
│                                                         │
│  • Prediction cards with scores                         │
│  • Gauge charts and radar plot                          │
│  • AI-generated advice                                  │
│  • Slack share button                                   │
│  • Voice summary button                                 │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 📦 File Locations

```
Your Project/
│
├── app.py                          ← Dashboard UI (what users see)
│
├── inua360_the_kenyan_sme_ai_agent/
│   └── modeling/
│       └── predictions_api.py      ← API backend (runs ML models)
│
├── models/                         ← ML model files (must exist!)
│   ├── best_funding_model.pkl
│   ├── best_compliance_risk_level_model.pkl
│   ├── growth_model.pkl
│   ├── funding_features.pkl
│   ├── compliance_features.pkl
│   └── growth_features.pkl
│
├── .env                           ← API secrets (create this!)
├── .streamlit/
│   └── secrets.toml               ← Dashboard secrets (create this!)
│
└── start_dashboard.bat            ← Click this to start everything!
```

---

## ⚠️ Common Issues

### "Model file not found"
**Problem:** ML models not in `models/` directory  
**Solution:** Ensure you've trained models or copied `.pkl` files to `models/`

### "Connection refused"
**Problem:** API not running  
**Solution:** Start API first: `python inua360_the_kenyan_sme_ai_agent\modeling\predictions_api.py`

### "OpenAI API error"
**Problem:** Missing or invalid API key  
**Solution:** Add real key to `.env` file: `OPENAI_API_KEY=sk-proj-...`

### "Port already in use"
**Problem:** Another app using port 8000 or 8501  
**Solution:** Stop other services or change port in code

---

## 🎉 You're Ready!

Just run:
```bash
start_dashboard.bat
```

Choose option **2**, and everything starts automatically!

Dashboard opens at: `http://localhost:8501`  
API docs at: `http://localhost:8000/docs`

**Happy analyzing! 🚀**
