"""
Inua360 Dashboard Configuration
Customize your dashboard settings here
"""

# API Configuration
API_ENDPOINTS = {
    "base_url": "https://inua360-the-kenyan-sme-ai-agent.onrender.com",
    "predict_sme": "/predict/sme",
    "predict_funding": "/predict/funding",
    "predict_compliance": "/predict/compliance",
    "predict_growth": "/predict/growth"
}

# n8n Webhook Configuration
N8N_WEBHOOKS = {
    "test": "https://abby218.app.n8n.cloud/webhook-test/sme-data",
    "production": "https://abby218.app.n8n.cloud/webhook/sme-data",
    "active": "production"  # Switch between "test" and "production"
}

# Slack Configuration
SLACK_CONFIG = {
    "enabled": True,
    "webhook_url": "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK",
    "channel": "#sme-insights",
    "username": "Inua360 Bot",
    "icon_emoji": ":rocket:"
}

# ElevenLabs Configuration
ELEVENLABS_CONFIG = {
    "enabled": False,
    "api_key": "",
    "voice_id": "21m00Tcm4TlvDq8ikWAM",  # Default voice
    "model_id": "eleven_monolingual_v1"
}

# Theme Configuration
THEME = {
    "primary_color": "#FF6B35",
    "secondary_color": "#FF8C42",
    "accent_color": "#FFA726",
    "background_gradient": ["#FFF5EB", "#FFE4CC", "#FFD9B3"],
    "font_family": "Inter"
}

# Chart Configuration
CHART_CONFIG = {
    "gauge_max": 100,
    "gauge_thresholds": {
        "low": 40,
        "medium": 70,
        "high": 90
    },
    "animation_duration": 500
}

# Form Defaults
FORM_DEFAULTS = {
    "annual_revenue": 1000000.0,
    "expenses_total": 700000.0,
    "num_employees": 10,
    "avg_employee_salary": 50000.0,
    "cash_flow_score": 70.0,
    "credit_score": 650.0,
    "customer_growth_rate": 15.0,
    "customer_retention_rate": 80.0,
    "traction_score": 65.0,
    "digital_spending_ratio": 0.25,
    "bookkeeping_quality": 70.0,
    "data_protection_score": 60.0,
    "financial_transparency_score": 75.0,
    "years_in_operation": 3.0,
    "profit_to_expense_ratio": 0.3
}

# Feature Flags
FEATURES = {
    "show_voice_summary": True,
    "show_slack_integration": True,
    "show_download_report": True,
    "show_radar_chart": True,
    "show_gauge_charts": True,
    "enable_animations": True,
    "enable_auto_n8n": True,
    "show_debug_info": False
}

# Timeout Configuration (seconds)
TIMEOUTS = {
    "api_request": 60,
    "n8n_webhook": 10,
    "slack_webhook": 5,
    "elevenlabs_api": 30
}

# Sector Options
SECTORS = [
    "agriculture",
    "technology",
    "retail",
    "manufacturing",
    "services",
    "healthcare",
    "education",
    "other"
]

# Country Options
COUNTRIES = [
    "Kenya",
    "Uganda",
    "Tanzania",
    "Rwanda",
    "Other"
]

# Kenya Regions
KENYA_REGIONS = [
    "Nairobi",
    "Mombasa",
    "Kisumu",
    "Nakuru",
    "Eldoret",
    "Other"
]

# Tech Adoption Levels
TECH_LEVELS = [
    "low",
    "moderate",
    "high",
    "cutting_edge"
]

# Prior Investment Options
INVESTMENT_STAGES = [
    "none",
    "angel",
    "seed",
    "series_a",
    "series_b_plus"
]

# Compliance Status Options
COMPLIANCE_STATUS = [
    "compliant",
    "pending",
    "non_compliant"
]

# License Status Options
LICENSE_STATUS = [
    "valid",
    "pending",
    "expired",
    "not_applicable"
]

# Remote Work Options
REMOTE_WORK_OPTIONS = [
    "no_policy",
    "hybrid",
    "fully_remote",
    "office_only"
]

# Messages
MESSAGES = {
    "welcome": "🚀 Welcome to Inua360 AI Advisor - Empowering Kenyan SMEs!",
    "loading": "🔮 AI is analyzing your business...",
    "success": "✨ Analysis Complete! Your AI insights are ready.",
    "error": "❌ An error occurred. Please try again.",
    "no_results": "Fill in your business details and click RUN AI ANALYSIS to get started!",
    "slack_success": "✅ Shared to Slack!",
    "slack_error": "⚠️ Configure Slack webhook URL in settings"
}

# Help Text
HELP_TEXT = {
    "annual_revenue": "Total revenue for the fiscal year in KES",
    "cash_flow_score": "0-100 scale representing cash flow health",
    "credit_score": "Business credit score (300-850)",
    "customer_growth_rate": "Percentage change in customer base",
    "traction_score": "Market presence and momentum (0-100)",
    "digital_spending_ratio": "Proportion of budget spent on digital tools",
    "bookkeeping_quality": "Quality of financial record keeping (0-100)",
    "data_protection_score": "Data security and privacy compliance (0-100)"
}
