# 🎯 Inua360 Dashboard - Quick Reference Guide

## 📍 What You Have Now

### ✅ Complete Application Components

1. **`app.py`** - Modern, interactive Streamlit dashboard with:
   - Vibrant orange theme with wow-factor animations
   - Two-panel layout (input form + results)
   - Real-time AI predictions for funding, compliance, and growth
   - Interactive charts (gauge, radar, bar charts)
   - Slack integration
   - ElevenLabs voice summary
   - n8n webhook automation

2. **`predictions_api.py`** - FastAPI backend with:
   - 4 ML model endpoints
   - OpenAI GPT-4 integration for advice generation
   - n8n webhook integration
   - Auto-generated API documentation

3. **Startup Scripts:**
   - `start_dashboard.bat` - Windows batch file with menu
   - `start.py` - Cross-platform Python launcher
   - `start_dashboard.sh` - Linux/Mac shell script

4. **Documentation:**
   - `STARTUP_GUIDE.md` - Complete setup instructions
   - `README_DASHBOARD.md` - Dashboard features overview
   - `test_sme_data.json` - Sample test data

---

## 🚀 How to Run (3 Options)

### Option 1: Quick Start (Recommended)

**Windows:**
```bash
start_dashboard.bat
```

**Mac/Linux or Python:**
```bash
python start.py
```

Choose option **2** to run both API and dashboard locally.

---

### Option 2: Manual Start (Two Terminals)

**Terminal 1 - Start API:**
```bash
python inua360_the_kenyan_sme_ai_agent\modeling\predictions_api.py
```

**Terminal 2 - Start Dashboard:**
```bash
streamlit run app.py
```

---

### Option 3: Use Deployed API

If API is already on Render:
```bash
streamlit run app.py
```

Dashboard automatically connects to:
`https://inua360-the-kenyan-sme-ai-agent.onrender.com`

---

## 🔑 Required Configuration

### 1. Create `.env` file (for API):
```env
OPENAI_API_KEY=sk-your-key-here
PORT=8000
```

### 2. Create `.streamlit/secrets.toml` (for Dashboard):
```toml
API_BASE_URL = "http://localhost:8000"
N8N_WEBHOOK_URL = "https://abby218.app.n8n.cloud/webhook/sme-data"
SLACK_WEBHOOK_URL = "your_slack_webhook_url"
ELEVENLABS_API_KEY = "your_elevenlabs_key"
ELEVENLABS_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"
```

> **Note:** The startup scripts will create template files if they don't exist!

---

## 📊 API Endpoints

All available at: `http://localhost:8000/docs` (when running locally)

| Endpoint | Description | Used By |
|----------|-------------|---------|
| `POST /predict/funding` | Funding readiness score | Individual predictions |
| `POST /predict/compliance` | Compliance risk assessment | Individual predictions |
| `POST /predict/growth` | Revenue growth projection | Individual predictions |
| `POST /predict/sme` | **Combined analysis** | **Dashboard uses this** |

---

## 🎨 Dashboard Features

### Left Panel - Input Form
- 28 business metrics with intelligent input types
- Real-time validation with color feedback
- Organized sections: Financial, Operational, Compliance, Business Profile
- Dynamic sliders, dropdowns, and toggles

### Right Panel - AI Insights
After clicking "🚀 Run AI Analysis":

1. **Prediction Cards**
   - 💰 Funding Readiness Score (0-100)
   - ⚖️ Compliance Score (0-100)
   - 📈 Growth Projection (%)

2. **Visual Analytics**
   - Gauge charts for each metric
   - Radar chart for overall health
   - Color-coded risk indicators

3. **AI-Powered Advice**
   - Executive summary
   - Strategic roadmap
   - Risk analysis
   - 14-day action plan
   - Kenya-specific opportunities

4. **Interactive Actions**
   - 📢 Share to Slack
   - 🎤 Listen to Voice Summary
   - 💾 Download JSON results

---

## 🔗 Integrations

### Slack
- Channel: [elevateai-global.slack.com](https://elevateai-global.slack.com/)
- Sends prediction summary with one click
- Webhook format: `https://hooks.slack.com/services/...`

### n8n Automation
- Test webhook: `https://abby218.app.n8n.cloud/webhook-test/sme-data`
- Production: `https://abby218.app.n8n.cloud/webhook/sme-data`
- Automatically receives all predictions

### ElevenLabs Voice
- Converts AI advice to natural speech
- Plays directly in browser
- Uses voice ID: `21m00Tcm4TlvDq8ikWAM`

---

## 🧪 Testing the API

### Test with curl:
```bash
curl -X POST "http://localhost:8000/predict/sme" ^
  -H "Content-Type: application/json" ^
  -d @test_sme_data.json
```

### Test in browser:
1. Open: `http://localhost:8000/docs`
2. Click on `POST /predict/sme`
3. Click "Try it out"
4. Use sample data from `test_sme_data.json`
5. Click "Execute"

---

## 📦 Project Structure

```
Inua360-The-Kenyan-SME-AI-Agent/
│
├── app.py                          # 🎨 Streamlit Dashboard (MAIN UI)
├── start.py                        # 🚀 Python launcher
├── start_dashboard.bat             # 🚀 Windows launcher
├── test_sme_data.json              # 🧪 Sample test data
│
├── inua360_the_kenyan_sme_ai_agent/
│   └── modeling/
│       └── predictions_api.py      # 🔧 FastAPI Backend (MAIN API)
│
├── models/                         # 🤖 Trained ML models
│   ├── best_funding_model.pkl
│   ├── best_compliance_risk_level_model.pkl
│   ├── growth_model.pkl
│   └── *_features.pkl
│
├── .env                           # 🔑 API secrets (create this)
├── .streamlit/
│   └── secrets.toml               # 🔑 Dashboard secrets (create this)
│
├── STARTUP_GUIDE.md               # 📚 Complete documentation
└── README_DASHBOARD.md            # 📚 Dashboard features
```

---

## 🎯 Hackathon Win Features

### 🏆 Wow Factors
1. **Interactive Animations** - Smooth transitions, hover effects, pulsing elements
2. **Real-time Validation** - Instant feedback as users type
3. **Voice AI Summary** - Listen to insights instead of reading
4. **One-Click Slack Share** - Instant team collaboration
5. **Beautiful Visualizations** - Gauge charts, radar plots, gradient cards
6. **AI-Powered Advice** - GPT-4 generates personalized strategies
7. **Kenyan Context** - Localized insights for Kenyan SMEs
8. **Automation Ready** - n8n integration for workflow automation

### 🎨 Design Highlights
- Vibrant orange theme (Kenya-inspired)
- Modern, professional UI with glassmorphism effects
- Responsive layout (desktop + tablet)
- Micro-interactions and hover states
- Clean typography with visual hierarchy
- Color-coded risk indicators

---

## ⚡ Performance Tips

1. **Local Development**: Use `http://localhost:8000` in secrets.toml
2. **Production**: Use deployed Render URL
3. **Fast Testing**: Use API docs at `/docs` for quick tests
4. **Debugging**: Check browser console + terminal logs
5. **Model Loading**: First request takes ~3-5s (model loading)

---

## 🐛 Troubleshooting Quick Fixes

| Issue | Solution |
|-------|----------|
| "Connection refused" | Start API: `python inua360_the_kenyan_sme_ai_agent\modeling\predictions_api.py` |
| "Model not found" | Ensure `.pkl` files in `models/` directory |
| "OpenAI error" | Check `OPENAI_API_KEY` in `.env` |
| "Streamlit error" | Check `API_BASE_URL` in `.streamlit/secrets.toml` |
| "n8n not receiving" | Verify webhook URL is correct |

---

## 📱 URLs at a Glance

**Local Development:**
- API: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
- Dashboard: `http://localhost:8501`

**Production:**
- API: `https://inua360-the-kenyan-sme-ai-agent.onrender.com`
- API Docs: `https://inua360-the-kenyan-sme-ai-agent.onrender.com/docs`
- Slack: `https://elevateai-global.slack.com/`
- n8n: `https://abby218.app.n8n.cloud/webhook/sme-data`

---

## 🎓 Demo Flow

1. **Open Dashboard**: Run `start_dashboard.bat` → Choose option 2
2. **Fill Form**: Enter SME details (use realistic values)
3. **Run Analysis**: Click "🚀 Run AI Analysis"
4. **Show Predictions**: Point out the 3 prediction cards
5. **Explain Charts**: Walk through gauge + radar visualizations
6. **Read AI Advice**: Highlight GPT-4 strategic insights
7. **Demo Slack**: Click "Share to Slack" button
8. **Play Voice**: Click "Listen to Voice Summary"
9. **Show API Docs**: Open `/docs` in browser
10. **Highlight Automation**: Mention n8n workflow triggers

---

## 🚀 Next Steps

1. ✅ Run `start_dashboard.bat` (or `python start.py`)
2. ✅ Choose option 2 (local development)
3. ✅ Open `http://localhost:8501`
4. ✅ Test with sample data
5. ✅ Configure API keys for full features
6. 🎉 Win the hackathon!

---

**Built with ❤️ for Kenyan SMEs | Powered by AI | Ready to Scale 🚀**
