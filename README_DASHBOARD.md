# 🚀 Inua360 AI-Powered SME Dashboard

A modern, interactive dashboard for Kenyan SMEs providing real-time, personalized insights on funding, compliance, and growth.

## ✨ Features

### 🎨 Beautiful Orange-Themed UI
- Vibrant, modern design with smooth animations
- Interactive micro-interactions and hover effects
- Responsive layout for desktop and tablet
- Dynamic color changes based on input values

### 🤖 AI-Powered Insights
- **Funding Predictions**: Get AI-driven funding readiness scores
- **Compliance Analysis**: Real-time compliance risk assessment
- **Growth Forecasts**: Predictive growth modeling
- **Tech Readiness**: Digital transformation evaluation
- **Overall Summary**: Comprehensive AI advisory report

### 📊 Interactive Visualizations
- Dynamic gauge charts for key metrics
- Radar charts for multi-dimensional analysis
- Animated bar charts with hover states
- Color-coded risk badges
- Progress indicators

### 🔗 Seamless Integrations
- **n8n Automation**: Automatic data workflow triggers
- **Slack Notifications**: Share insights with your team
- **ElevenLabs Voice**: AI-generated voice summaries
- **FastAPI Backend**: Real-time predictions

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/Inua360-The-Kenyan-SME-AI-Agent.git
cd Inua360-The-Kenyan-SME-AI-Agent
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure secrets** (Optional)
Edit `.streamlit/secrets.toml` to add:
- Slack webhook URL
- ElevenLabs API key
- Custom n8n webhook URLs

### Running the Dashboard

**Option 1: Using Streamlit directly**
```bash
streamlit run app.py
```

**Option 2: Using the start script**
```bash
bash start.sh
```

The dashboard will open automatically in your browser at `http://localhost:8501`

## 📋 Usage Guide

### Step 1: Input Business Data
Fill in the comprehensive form on the left panel:

#### 💰 Financial Health
- Annual Revenue
- Total Expenses
- Cash Flow Score
- Credit Score
- Profit/Expense Ratio
- Financial Transparency Score

#### 👥 Operations & Team
- Number of Employees
- Average Employee Salary
- Years in Operation
- Employee Contracts Status
- Remote Work Policy
- Business Registration Status

#### 📈 Market & Growth
- Customer Growth Rate
- Customer Retention Rate
- Market Traction Score
- Digital Spending Ratio
- Tech Adoption Level

#### ⚖️ Compliance & Governance
- Bookkeeping Quality
- Data Protection Score
- Tax Compliance Status
- Regulatory License Status
- AML Risk Flag

#### 🏢 Business Profile
- Sector
- Country & Region
- Female-Owned Status
- Pitch Deck Availability
- Prior Investment History

### Step 2: Run AI Analysis
Click the **🚀 RUN AI ANALYSIS** button to:
1. Send data to the AI prediction API
2. Trigger n8n automation workflows
3. Generate comprehensive insights

### Step 3: Review Insights
The right panel displays:
- **Metric Cards**: Quick scores for Funding, Compliance, and Growth
- **Gauge Charts**: Visual funding readiness and compliance scores
- **Radar Chart**: Multi-dimensional business health overview
- **AI Advisory Report**: Detailed recommendations and strategies

### Step 4: Take Action
- **📢 Share to Slack**: Send results to your team
- **🎙️ Listen to Summary**: Get AI voice summary (ElevenLabs)
- **📊 Download Report**: Export results as JSON

## 🔗 API Endpoints

The dashboard connects to the following endpoints:

### Base URL
```
https://inua360-the-kenyan-sme-ai-agent.onrender.com
```

### Endpoints
- `POST /predict/sme` - Combined predictions (funding, compliance, growth)
- `POST /predict/funding` - Funding prediction only
- `POST /predict/compliance` - Compliance prediction only
- `POST /predict/growth` - Growth prediction only

### Documentation
Visit the interactive API docs:
```
https://inua360-the-kenyan-sme-ai-agent.onrender.com/docs
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file with:
```env
OPENAI_API_KEY=your_openai_api_key
```

### Streamlit Secrets
Edit `.streamlit/secrets.toml`:
```toml
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK"
ELEVENLABS_API_KEY = "your_elevenlabs_api_key"
N8N_WEBHOOK_PROD = "https://abby218.app.n8n.cloud/webhook/sme-data"
```

## 🌐 Integration Details

### n8n Workflow Automation
Every analysis automatically triggers n8n workflows:
- **Test URL**: `https://abby218.app.n8n.cloud/webhook-test/sme-data`
- **Production URL**: `https://abby218.app.n8n.cloud/webhook/sme-data`

Data sent includes:
- Timestamp
- Input parameters
- Predictions
- AI advice

### Slack Integration
Configure webhook in secrets.toml to receive:
- Analysis completion notifications
- Key metric summaries
- Direct links to full reports

### ElevenLabs Voice
Enable voice summaries by adding API key to secrets.toml

## 🎨 Design Features

### Animations & Effects
- ✨ Slide-down header animation
- 🎯 Fade-in card animations
- 💫 Pulse effects on key elements
- 🌊 Gradient shifting background
- 🎪 Bounce-in badges
- 🚀 Scale transforms on hover

### Color Palette
- Primary Orange: `#FF6B35`
- Secondary Orange: `#FF8C42`
- Accent Orange: `#FFA726`
- Light Orange: `#FFD9B3`
- Very Light: `#FFE4CC`
- Background: `#FFF5EB`

### Interactive Elements
- Dynamic form validation
- Real-time color feedback
- Progress bars with animations
- Tooltip explanations
- Expandable detail cards

## 📱 Responsive Design
- Optimized for desktop (1920x1080)
- Tablet-friendly (768px+)
- Consistent spacing and typography
- Touch-friendly buttons

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License
MIT License - feel free to use this project for your hackathon or production needs.

## 🏆 Built For
**ElevateAI Global Hackathon**
- Empowering Kenyan SMEs with AI
- Winning with innovation and user experience
- Creating real impact for African businesses

## 📞 Support
- Slack: [Join ElevateAI Global](https://elevateai-global.slack.com/)
- API Docs: [View Documentation](https://inua360-the-kenyan-sme-ai-agent.onrender.com/docs)

## 🎉 Acknowledgments
Built with:
- Streamlit
- FastAPI
- Plotly
- n8n
- OpenAI
- ElevenLabs
- ❤️ and lots of coffee

---

**Made with 🧡 for Kenyan SMEs | Inua360 © 2025**
