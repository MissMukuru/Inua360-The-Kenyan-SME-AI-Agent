# 🚀 Inua360 SME AI Agent - Complete Startup Guide

## 📋 Prerequisites

Before running the application, ensure you have:

1. **Python 3.8+** installed
2. **pip** package manager
3. **Trained ML models** in the `models/` directory:
   - `best_funding_model.pkl`
   - `best_compliance_risk_level_model.pkl`
   - `growth_model.pkl`
   - `funding_features.pkl`
   - `compliance_features.pkl`
   - `growth_features.pkl`

4. **API Keys** (required for full functionality):
   - OpenAI API key (for AI advice generation)
   - ElevenLabs API key (for voice summaries)
   - Slack webhook URL (for notifications)

---

## 🎯 Two Ways to Run the Application

### **Option 1: Run API + Dashboard Separately (Recommended for Development)**

#### Step 1: Start the FastAPI Backend

The FastAPI backend serves the ML models and handles predictions.

```bash
# Navigate to the project directory
cd c:\projects\Inua360-The-Kenyan-SME-AI-Agent

# Install dependencies
pip install -r requirements.txt

# Set environment variables (Windows CMD)
set OPENAI_API_KEY=your_openai_api_key_here
set PORT=8000

# Or create a .env file with:
# OPENAI_API_KEY=your_openai_api_key_here
# PORT=8000

# Run the FastAPI server
python inua360_the_kenyan_sme_ai_agent\modeling\predictions_api.py
```

**The API will be available at:**
- Local: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

**Available API Endpoints:**
- `POST /predict/funding` - Funding readiness prediction
- `POST /predict/compliance` - Compliance risk assessment
- `POST /predict/growth` - Revenue growth projection
- `POST /predict/sme` - **Combined analysis (used by dashboard)**

#### Step 2: Start the Streamlit Dashboard

Open a **new terminal** and run:

```bash
# Navigate to the project directory
cd c:\projects\Inua360-The-Kenyan-SME-AI-Agent

# Run the Streamlit app
streamlit run app.py
```

**The dashboard will open at:** `http://localhost:8501`

---

### **Option 2: Use Deployed API (Production)**

If the API is already deployed on Render:

```bash
# Just run the Streamlit dashboard
streamlit run app.py
```

The app is configured to use:
- **API:** `https://inua360-the-kenyan-sme-ai-agent.onrender.com`
- **n8n Webhook:** `https://abby218.app.n8n.cloud/webhook/sme-data`

---

## ⚙️ Configuration Setup

### 1. Create `.env` File (for API)

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=sk-your-openai-api-key-here
PORT=8000
```

### 2. Create `.streamlit/secrets.toml` (for Dashboard)

Create the secrets file for Streamlit:

```bash
mkdir .streamlit
```

Create `.streamlit/secrets.toml`:

```toml
# API Configuration
API_BASE_URL = "http://localhost:8000"  # Use this for local development
# API_BASE_URL = "https://inua360-the-kenyan-sme-ai-agent.onrender.com"  # Use this for production

N8N_WEBHOOK_URL = "https://abby218.app.n8n.cloud/webhook/sme-data"

# Slack Integration
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK"
SLACK_CHANNEL = "elevateai-global.slack.com"

# ElevenLabs Voice API
ELEVENLABS_API_KEY = "your_elevenlabs_api_key_here"
ELEVENLABS_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Default voice
```

---

## 🎨 Running the Complete Application

### Quick Start (Both Services)

Use the provided batch file:

```bash
# Windows
start_dashboard.bat
```

Or run manually in **two separate terminals**:

**Terminal 1 - API Server:**
```bash
python inua360_the_kenyan_sme_ai_agent\modeling\predictions_api.py
```

**Terminal 2 - Streamlit Dashboard:**
```bash
streamlit run app.py
```

---

## 📊 Using the Dashboard

### Left Panel: Input SME Data
1. Fill in all business metrics (revenue, expenses, employees, etc.)
2. Use sliders, dropdowns, and toggles for easy input
3. Each field validates in real-time with color feedback

### Right Panel: AI Insights
After clicking **"🚀 Run AI Analysis"**:

1. **Prediction Cards:** View funding readiness, compliance score, and growth projection
2. **Gauge Charts:** Visual representation of each metric
3. **Radar Chart:** Overall business health snapshot
4. **AI Advice:** Personalized recommendations from GPT-4
5. **Action Buttons:**
   - 📢 Share to Slack
   - 🎤 Listen to Voice Summary (via ElevenLabs)

---

## 🔗 API Integration Details

### Endpoint: `POST /predict/sme`

**Request Body Example:**
```json
{
  "annual_revenue": 5000000,
  "expenses_total": 3000000,
  "num_employees": 25,
  "avg_employee_salary": 60000,
  "customer_growth_rate": 15.5,
  "customer_retention_rate": 85.0,
  "digital_spending_ratio": 20.0,
  "profit_to_expense_ratio": 0.67,
  "cash_flow_score": 7.5,
  "credit_score": 720,
  "traction_score": 8.0,
  "bookkeeping_quality": 8.5,
  "data_protection_score": 7.0,
  "financial_transparency_score": 8.0,
  "AML_risk_flag": 0,
  "has_pitch_deck": 1,
  "registered_business": 1,
  "female_owned": 1,
  "employee_contracts_verified": 1,
  "years_in_operation": 5.0,
  "tech_adoption_level": "High",
  "sector": "Technology",
  "country": "Kenya",
  "region": "East Africa",
  "prior_investment": "Seed",
  "tax_compliance_status": "Compliant",
  "regulatory_license_status": "Active",
  "remote_work_policy": "Hybrid"
}
```

**Response Example:**
```json
{
  "predictions": {
    "funding": 85,
    "compliance": 78,
    "growth": 23.5
  },
  "overall_advice": "# Executive Summary\n\nYour SME shows strong potential with excellent funding readiness (85/100)...\n\n## Inua360 Insight\n\n...\n\n## Strategic Roadmap\n\n..."
}
```

---

## 🧪 Testing the API

### Using the Interactive Docs

1. Open: `http://localhost:8000/docs`
2. Click on `POST /predict/sme`
3. Click **"Try it out"**
4. Modify the example JSON
5. Click **"Execute"**

### Using curl

```bash
curl -X POST "http://localhost:8000/predict/sme" \
  -H "Content-Type: application/json" \
  -d @test_data.json
```

### Using Python

```python
import requests

url = "http://localhost:8000/predict/sme"
data = {
    "annual_revenue": 5000000,
    "expenses_total": 3000000,
    # ... rest of fields
}

response = requests.post(url, json=data)
print(response.json())
```

---

## 🐛 Troubleshooting

### Issue: "Connection refused" or API not responding
**Solution:** Ensure the FastAPI server is running on port 8000
```bash
python inua360_the_kenyan_sme_ai_agent\modeling\predictions_api.py
```

### Issue: "Model file not found"
**Solution:** Ensure all `.pkl` files are in the `models/` directory

### Issue: "OpenAI API error"
**Solution:** Check your `.env` file has valid `OPENAI_API_KEY`

### Issue: Streamlit shows "Connection error"
**Solution:** Check `API_BASE_URL` in `.streamlit/secrets.toml` points to running API

### Issue: n8n webhook not receiving data
**Solution:** Verify the webhook URL is correct:
- Test: `https://abby218.app.n8n.cloud/webhook-test/sme-data`
- Production: `https://abby218.app.n8n.cloud/webhook/sme-data`

---

## 🚀 Deployment

### Deploy API to Render

1. Push code to GitHub
2. Create new Web Service on Render
3. Set environment variables:
   - `OPENAI_API_KEY`
   - `PORT=8000`
4. Build command: `pip install -r requirements.txt`
5. Start command: `python inua360_the_kenyan_sme_ai_agent/modeling/predictions_api.py`

### Deploy Dashboard to Streamlit Cloud

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Deploy from repository
4. Add secrets in Streamlit Cloud dashboard
5. Set main file: `app.py`

---

## 📱 Slack Integration

The app sends analysis results to Slack via webhook:

1. Create Slack webhook at: `https://api.slack.com/apps`
2. Add webhook URL to `.streamlit/secrets.toml`
3. Click "📢 Share to Slack" button in dashboard

**Slack Channel:** [elevateai-global.slack.com](https://elevateai-global.slack.com/)

---

## 🎤 Voice Summary Feature

The ElevenLabs integration provides AI voice summaries:

1. Sign up at [elevenlabs.io](https://elevenlabs.io)
2. Get API key and add to secrets
3. Click "🎤 Listen to Voice Summary" in dashboard
4. Audio plays automatically with AI-generated insights

---

## 📦 Project Structure

```
Inua360-The-Kenyan-SME-AI-Agent/
├── app.py                          # Streamlit dashboard (main UI)
├── inua360_the_kenyan_sme_ai_agent/
│   └── modeling/
│       └── predictions_api.py      # FastAPI backend (ML models)
├── models/                         # Trained ML models (.pkl files)
├── .env                           # API environment variables
├── .streamlit/
│   └── secrets.toml               # Dashboard secrets
├── requirements.txt               # Python dependencies
└── STARTUP_GUIDE.md              # This file
```

---

## 🎯 Next Steps

1. ✅ Install dependencies: `pip install -r requirements.txt`
2. ✅ Set up `.env` and `.streamlit/secrets.toml`
3. ✅ Start API server: `python inua360_the_kenyan_sme_ai_agent\modeling\predictions_api.py`
4. ✅ Start dashboard: `streamlit run app.py`
5. ✅ Open browser: `http://localhost:8501`
6. 🎉 Start analyzing SMEs!

---

## 💡 Pro Tips

- Use **local API** during development for faster debugging
- Use **deployed API** for production/demo
- Check API docs at `/docs` for detailed endpoint information
- Monitor n8n workflow for automation triggers
- Test with various SME profiles to see different predictions

---

## 📞 Support

For issues or questions:
- Check API logs for backend errors
- Check browser console for frontend errors
- Verify all environment variables are set
- Ensure models are trained and saved in `models/`

**Happy analyzing! 🚀**
