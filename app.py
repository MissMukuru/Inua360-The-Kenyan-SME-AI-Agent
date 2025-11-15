import streamlit as st
import requests
import json
import time
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any
import base64
from pathlib import Path

# =============================
# PAGE CONFIG & CUSTOM CSS
# =============================
st.set_page_config(
    page_title="Inua360 | AI-Powered SME Advisor",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for vibrant orangeish theme with wow effects
st.markdown("""
<style>
    /* Global styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main background with gradient */
    .stApp {
        background: linear-gradient(135deg, #FFF5EB 0%, #FFE4CC 50%, #FFD9B3 100%);
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #FF6B35 0%, #FF8C42 50%, #FFA726 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(255, 107, 53, 0.3);
        margin-bottom: 2rem;
        animation: slideDown 0.8s ease-out;
        text-align: center;
    }
    
    @keyframes slideDown {
        from { transform: translateY(-50px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    .main-header h1 {
        color: white;
        font-size: 3rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    .main-header p {
        color: #FFF5EB;
        font-size: 1.2rem;
        margin-top: 0.5rem;
    }
    
    /* Input card styling */
    .input-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(255, 107, 53, 0.15);
        border: 2px solid #FFD9B3;
        transition: all 0.3s ease;
        animation: fadeInLeft 0.8s ease-out;
    }
    
    @keyframes fadeInLeft {
        from { transform: translateX(-30px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    .input-card:hover {
        box-shadow: 0 12px 48px rgba(255, 107, 53, 0.25);
        transform: translateY(-5px);
    }
    
    /* Result card styling */
    .result-card {
        background: linear-gradient(135deg, #FFFFFF 0%, #FFF8F0 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 6px 24px rgba(255, 107, 53, 0.12);
        border-left: 5px solid #FF6B35;
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
        animation: fadeInRight 0.8s ease-out;
    }
    
    @keyframes fadeInRight {
        from { transform: translateX(30px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    .result-card:hover {
        box-shadow: 0 10px 36px rgba(255, 107, 53, 0.2);
        transform: translateX(5px);
    }
    
    /* Badge styling */
    .badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-weight: 700;
        font-size: 0.9rem;
        margin: 0.5rem 0.5rem 0.5rem 0;
        animation: bounceIn 0.6s ease-out;
    }
    
    @keyframes bounceIn {
        0% { transform: scale(0); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    
    .badge-success {
        background: linear-gradient(135deg, #4CAF50, #66BB6A);
        color: white;
        box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
    }
    
    .badge-warning {
        background: linear-gradient(135deg, #FFA726, #FFB74D);
        color: white;
        box-shadow: 0 4px 12px rgba(255, 167, 38, 0.3);
    }
    
    .badge-danger {
        background: linear-gradient(135deg, #EF5350, #E57373);
        color: white;
        box-shadow: 0 4px 12px rgba(239, 83, 80, 0.3);
    }
    
    .badge-info {
        background: linear-gradient(135deg, #29B6F6, #4FC3F7);
        color: white;
        box-shadow: 0 4px 12px rgba(41, 182, 246, 0.3);
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #FF6B35 0%, #FF8C42 100%);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 1rem 3rem;
        font-size: 1.1rem;
        font-weight: 700;
        box-shadow: 0 6px 20px rgba(255, 107, 53, 0.4);
        transition: all 0.3s ease;
        cursor: pointer;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Advice section styling */
    .advice-section {
        background: linear-gradient(135deg, #FFFFFF 0%, #FFF5EB 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        border-left: 6px solid #FF6B35;
        box-shadow: 0 8px 32px rgba(255, 107, 53, 0.15);
        animation: fadeInUp 0.8s ease-out;
    }
    
    @keyframes fadeInUp {
        from { transform: translateY(30px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    .advice-section h3 {
        color: #FF6B35;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .advice-section h4 {
        color: #FF8C42;
        font-size: 1.2rem;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
    }
    
    .advice-section p {
        color: #333;
        line-height: 1.8;
        font-size: 1.05rem;
        margin-bottom: 1rem;
    }
    
    .advice-section ul {
        list-style: none;
        padding-left: 0;
    }
    
    .advice-section li {
        color: #444;
        padding: 0.5rem 0;
        padding-left: 1.5rem;
        position: relative;
        line-height: 1.6;
    }
    
    .advice-section li:before {
        content: "🔸";
        position: absolute;
        left: 0;
    }
    
    .personalized-greeting {
        background: linear-gradient(135deg, #FF6B35 0%, #FFA726 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 40px rgba(255, 107, 53, 0.3);
        animation: slideDown 0.8s ease-out;
    }
    
    .personalized-greeting h2 {
        font-size: 2rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .personalized-greeting p {
        font-size: 1.1rem;
        margin-top: 0.5rem;
        opacity: 0.95;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 10px 30px rgba(255, 107, 53, 0.6);
        background: linear-gradient(135deg, #FF8C42 0%, #FFA726 100%);
    }
    
    .stButton>button:active {
        transform: translateY(-1px);
    }
    
    /* Input field styling */
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stSelectbox>div>div>select {
        border: 2px solid #FFD9B3;
        border-radius: 10px;
        padding: 0.75rem;
        transition: all 0.3s ease;
        background: #FFFAF5;
    }
    
    .stTextInput>div>div>input:focus,
    .stNumberInput>div>div>input:focus,
    .stSelectbox>div>div>select:focus {
        border-color: #FF6B35;
        box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.1);
        background: white;
    }
    
    /* Slider styling */
    .stSlider>div>div>div>div {
        background: linear-gradient(90deg, #FF6B35, #FFA726);
    }
    
    /* Loading animation */
    .loading-spinner {
        display: inline-block;
        width: 50px;
        height: 50px;
        border: 5px solid #FFD9B3;
        border-top: 5px solid #FF6B35;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Metric card */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 16px rgba(255, 107, 53, 0.1);
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }
    
    .metric-card:hover {
        border-color: #FF6B35;
        transform: scale(1.05);
        box-shadow: 0 8px 24px rgba(255, 107, 53, 0.2);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #FF6B35;
        margin: 0;
    }
    
    .metric-label {
        font-size: 1rem;
        color: #666;
        margin-top: 0.5rem;
    }
    
    /* Section headers */
    .section-header {
        color: #FF6B35;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #FFD9B3;
    }
    
    /* Advice box */
    .advice-box {
        background: linear-gradient(135deg, #FFF8F0 0%, #FFFFFF 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #FF8C42;
        margin: 1rem 0;
        box-shadow: 0 4px 16px rgba(255, 107, 53, 0.1);
        animation: fadeIn 1s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Sparkle effect */
    @keyframes sparkle {
        0%, 100% { opacity: 0; transform: scale(0); }
        50% { opacity: 1; transform: scale(1); }
    }
    
    .sparkle {
        animation: sparkle 1.5s ease-in-out infinite;
    }
    
    /* Success message */
    .success-message {
        background: linear-gradient(135deg, #4CAF50, #66BB6A);
        color: white;
        padding: 1rem 2rem;
        border-radius: 15px;
        text-align: center;
        font-weight: 600;
        box-shadow: 0 6px 20px rgba(76, 175, 80, 0.3);
        animation: slideInUp 0.5s ease-out;
    }
    
    @keyframes slideInUp {
        from { transform: translateY(30px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    /* Personalized Greeting */
    .personalized-greeting {
        background: linear-gradient(135deg, #FF6B35 0%, #FF8C42 50%, #FFA726 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(255, 107, 53, 0.3);
        animation: bounceIn 0.8s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .personalized-greeting::before {
        content: '✨';
        position: absolute;
        top: 1rem;
        right: 1rem;
        font-size: 2rem;
        animation: sparkle 2s ease-in-out infinite;
    }
    
    .personalized-greeting h2 {
        margin: 0;
        font-size: 2rem;
        font-weight: 800;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .personalized-greeting p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.95;
    }
    
    @keyframes bounceIn {
        0% { transform: scale(0.8); opacity: 0; }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); opacity: 1; }
    }
    
    /* Progress bar */
    .progress-bar {
        background: #FFE4CC;
        height: 8px;
        border-radius: 10px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .progress-fill {
        background: linear-gradient(90deg, #FF6B35, #FFA726);
        height: 100%;
        transition: width 0.5s ease;
        box-shadow: 0 0 10px rgba(255, 107, 53, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# =============================
# CONFIGURATION
# =============================
API_BASE_URL = "https://inua360-the-kenyan-sme-ai-agent.onrender.com"
N8N_WEBHOOK_URL = "https://abby218.app.n8n.cloud/webhook/sme-data"
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK"  # Configure in secrets
ELEVENLABS_API_KEY = st.secrets.get("ELEVENLABS_API_KEY", "")  # Configure in secrets

# =============================
# HELPER FUNCTIONS
# =============================

def create_gauge_chart(value: float, title: str, max_value: float = 100) -> go.Figure:
    """Create a beautiful gauge chart with orange theme"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        title={'text': title, 'font': {'size': 20, 'color': '#FF6B35'}},
        delta={'reference': max_value * 0.7},
        gauge={
            'axis': {'range': [None, max_value], 'tickwidth': 1, 'tickcolor': "#FF6B35"},
            'bar': {'color': "#FF6B35"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "#FFD9B3",
            'steps': [
                {'range': [0, max_value * 0.33], 'color': '#FFE4CC'},
                {'range': [max_value * 0.33, max_value * 0.66], 'color': '#FFD9B3'},
                {'range': [max_value * 0.66, max_value], 'color': '#FFC299'}
            ],
            'threshold': {
                'line': {'color': "#FF8C42", 'width': 4},
                'thickness': 0.75,
                'value': max_value * 0.8
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': "#333", 'family': "Inter"},
        height=250
    )
    return fig

def create_bar_chart(data: Dict[str, float], title: str) -> go.Figure:
    """Create an animated bar chart"""
    fig = go.Figure(data=[
        go.Bar(
            x=list(data.keys()),
            y=list(data.values()),
            marker=dict(
                color=list(data.values()),
                colorscale=[[0, '#FFE4CC'], [0.5, '#FF8C42'], [1, '#FF6B35']],
                line=dict(color='#FF6B35', width=2)
            ),
            text=list(data.values()),
            textposition='outside',
            texttemplate='%{text:.1f}',
            hovertemplate='<b>%{x}</b><br>Score: %{y:.2f}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title={'text': title, 'font': {'size': 24, 'color': '#FF6B35', 'family': 'Inter'}},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'family': "Inter"},
        xaxis={'showgrid': False, 'showline': True, 'linecolor': '#FFD9B3'},
        yaxis={'showgrid': True, 'gridcolor': '#FFE4CC', 'showline': True, 'linecolor': '#FFD9B3'},
        height=400
    )
    return fig

def create_radar_chart(categories: list, values: list, title: str) -> go.Figure:
    """Create a radar chart for multi-dimensional analysis"""
    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(255, 107, 53, 0.3)',
        line=dict(color='#FF6B35', width=3),
        marker=dict(size=8, color='#FF8C42')
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                showticklabels=True,
                gridcolor='#FFD9B3'
            ),
            angularaxis=dict(gridcolor='#FFE4CC')
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        title={'text': title, 'font': {'size': 20, 'color': '#FF6B35'}},
        font={'family': "Inter"},
        height=400
    )
    return fig

def get_risk_badge(score: float, threshold_low: float = 40, threshold_high: float = 70) -> str:
    """Return HTML badge based on score"""
    if score < threshold_low:
        return '<span class="badge badge-danger">⚠️ High Risk</span>'
    elif score < threshold_high:
        return '<span class="badge badge-warning">⚡ Moderate Risk</span>'
    else:
        return '<span class="badge badge-success">✅ Low Risk</span>'

def send_to_slack(message: str, webhook_url: str = None):
    """Send notification to Slack"""
    try:
        url = webhook_url or SLACK_WEBHOOK_URL
        if not url or url == "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK":
            return False
        payload = {"text": message}
        response = requests.post(url, json=payload, timeout=5)
        return response.status_code == 200
    except:
        return False

def send_to_n8n(data: dict):
    """Send data to n8n webhook"""
    try:
        response = requests.post(N8N_WEBHOOK_URL, json=data, timeout=10)
        return response.status_code == 200
    except:
        return False

def generate_voice_summary(text: str):
    """Generate voice summary using ElevenLabs (placeholder)"""
    # This would integrate with ElevenLabs API
    st.info("🎙️ Voice summary generation would be triggered here with ElevenLabs API")
    return None

def format_advice_with_styling(advice: str) -> str:
    """Format AI advice with beautiful styling"""
    # Replace markdown with styled HTML
    advice = advice.replace('**', '')
    
    # Split into sections
    lines = advice.split('\n')
    formatted_html = '<div style="font-family: Inter; color: #333; line-height: 1.8;">'
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Main headers (##)
        if line.startswith('## '):
            title = line.replace('## ', '')
            formatted_html += f'''
            <div style="margin-top: 2rem; margin-bottom: 1rem;">
                <h3 style="color: #FF6B35; font-size: 1.5rem; font-weight: 700; border-left: 5px solid #FF8C42; padding-left: 1rem; margin-bottom: 0.5rem;">
                    {title}
                </h3>
            </div>
            '''
        # Sub-headers (###)
        elif line.startswith('### '):
            title = line.replace('### ', '')
            formatted_html += f'''
            <h4 style="color: #FF8C42; font-size: 1.2rem; font-weight: 600; margin-top: 1.5rem; margin-bottom: 0.5rem;">
                {title}
            </h4>
            '''
        # Bullet points
        elif line.startswith('- ') or line.startswith('• '):
            text = line.replace('- ', '').replace('• ', '')
            formatted_html += f'''
            <div style="margin-left: 1.5rem; margin-bottom: 0.5rem;">
                <span style="color: #FF6B35; font-weight: bold;">▸</span> 
                <span style="margin-left: 0.5rem;">{text}</span>
            </div>
            '''
        # Numbered lists
        elif line[0:2].replace('.', '').isdigit():
            formatted_html += f'''
            <div style="margin-left: 1.5rem; margin-bottom: 0.5rem;">
                <span style="color: #FF6B35; font-weight: bold;">{line.split('.')[0]}.</span> 
                <span style="margin-left: 0.5rem;">{'.'.join(line.split('.')[1:])}</span>
            </div>
            '''
        # Regular paragraphs
        else:
            formatted_html += f'''
            <p style="margin-bottom: 1rem; text-align: justify;">
                {line}
            </p>
            '''
    
    formatted_html += '</div>'
    return formatted_html

# =============================
# MAIN APP
# =============================

def main():
    # Header
    st.markdown("""
        <div class="main-header">
            <h1>🚀 Inua360 AI Advisor</h1>
            <p>Empowering Kenyan SMEs with AI-Driven Insights</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False
    if 'results' not in st.session_state:
        st.session_state.results = None
    
    # Two-column layout
    col_left, col_right = st.columns([1, 1], gap="large")
    
    # =============================
    # LEFT PANEL - INPUT FORM
    # =============================
    with col_left:
        st.markdown('<div class="input-card">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-header">📊 Business Information</h2>', unsafe_allow_html=True)
        
        with st.form("sme_input_form"):
            # Personalization Section
            st.markdown("### 👋 Welcome! Let's Get to Know Your Business")
            st.markdown('<div style="background: linear-gradient(135deg, #FFE4CC, #FFD9B3); padding: 1.5rem; border-radius: 15px; margin-bottom: 1.5rem;">', unsafe_allow_html=True)
            
            business_name = st.text_input("🏢 Business Name *", placeholder="e.g., Nairobi Tech Solutions", 
                                         help="Enter your registered business name")
            owner_name = st.text_input("👤 Your Name (optional)", placeholder="e.g., Jane Wanjiru", 
                                      help="Your full name or business owner name")
            
            col_contact1, col_contact2 = st.columns(2)
            with col_contact1:
                contact_email = st.text_input("📧 Email (optional)", placeholder="jane@example.com")
            with col_contact2:
                slack_webhook = st.text_input("🔗 Slack Webhook URL (optional)", 
                                             placeholder="https://hooks.slack.com/...",
                                             help="Paste your Slack webhook to receive results")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Financial Metrics
            st.markdown("### 💰 Financial Health")
            col1, col2 = st.columns(2)
            with col1:
                annual_revenue = st.number_input("Annual Revenue (KES)", min_value=0.0, value=1000000.0, step=10000.0, 
                                                help="Total revenue for the fiscal year")
                expenses_total = st.number_input("Total Expenses (KES)", min_value=0.0, value=700000.0, step=10000.0)
                cash_flow_score = st.slider("Cash Flow Score", 0.0, 100.0, 70.0, help="0-100 scale")
            with col2:
                credit_score = st.slider("Credit Score", 300.0, 850.0, 650.0)
                profit_to_expense_ratio = st.slider("Profit/Expense Ratio", 0.0, 2.0, 0.3, 0.01)
                financial_transparency_score = st.slider("Financial Transparency", 0.0, 100.0, 75.0)
            
            # Operational Metrics
            st.markdown("### 👥 Operations & Team")
            col3, col4 = st.columns(2)
            with col3:
                num_employees = st.number_input("Number of Employees", min_value=1, value=10, step=1)
                avg_employee_salary = st.number_input("Avg Employee Salary (KES)", min_value=0.0, value=50000.0, step=5000.0)
                years_in_operation = st.number_input("Years in Operation", min_value=0.0, value=3.0, step=0.5)
            with col4:
                employee_contracts_verified = st.checkbox("Employee Contracts Verified", value=True)
                remote_work_policy = st.selectbox("Remote Work Policy", 
                    ["no_policy", "hybrid", "fully_remote", "office_only"])
                registered_business = st.checkbox("Registered Business", value=True)
            
            # Market Performance
            st.markdown("### 📈 Market & Growth")
            col5, col6 = st.columns(2)
            with col5:
                customer_growth_rate = st.slider("Customer Growth Rate (%)", -50.0, 200.0, 15.0)
                customer_retention_rate = st.slider("Customer Retention Rate (%)", 0.0, 100.0, 80.0)
                traction_score = st.slider("Market Traction Score", 0.0, 100.0, 65.0)
            with col6:
                digital_spending_ratio = st.slider("Digital Spending Ratio", 0.0, 1.0, 0.25, 0.01)
                tech_adoption_level = st.selectbox("Tech Adoption Level", 
                    ["low", "moderate", "high", "cutting_edge"])
            
            # Compliance & Governance
            st.markdown("### ⚖️ Compliance & Governance")
            col7, col8 = st.columns(2)
            with col7:
                bookkeeping_quality = st.slider("Bookkeeping Quality", 0.0, 100.0, 70.0)
                data_protection_score = st.slider("Data Protection Score", 0.0, 100.0, 60.0)
                tax_compliance_status = st.selectbox("Tax Compliance Status", 
                    ["compliant", "pending", "non_compliant"])
            with col8:
                regulatory_license_status = st.selectbox("Regulatory License", 
                    ["valid", "pending", "expired", "not_applicable"])
                AML_risk_flag = st.checkbox("AML Risk Flag", value=False)
            
            # Business Profile
            st.markdown("### 🏢 Business Profile")
            col9, col10 = st.columns(2)
            with col9:
                sector = st.selectbox("Sector", 
                    ["agriculture", "technology", "retail", "manufacturing", "services", "healthcare", "education", "other"])
                country = st.selectbox("Country", ["Kenya", "Uganda", "Tanzania", "Rwanda", "Other"])
                region = st.selectbox("Region", ["Nairobi", "Mombasa", "Kisumu", "Nakuru", "Other"])
            with col10:
                female_owned = st.checkbox("Female-Owned", value=False)
                has_pitch_deck = st.checkbox("Has Pitch Deck", value=True)
                prior_investment = st.selectbox("Prior Investment", 
                    ["none", "angel", "seed", "series_a", "series_b_plus"])
            
            # Submit Button
            st.markdown("<br>", unsafe_allow_html=True)
            submit_button = st.form_submit_button("🚀 RUN AI ANALYSIS", use_container_width=True)
            
            # Validation message
            if submit_button and not business_name:
                st.error("⚠️ Please enter your business name to continue.")
                submit_button = False
            if submit_button and not owner_name:
                st.error("⚠️ Please enter your name to continue.")
                submit_button = False
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # =============================
    # RIGHT PANEL - RESULTS
    # =============================
    with col_right:
        if submit_button:
            # Store personalization in session
            st.session_state.business_name = business_name
            st.session_state.owner_name = owner_name
            st.session_state.contact_email = contact_email
            st.session_state.slack_webhook = slack_webhook
            
            # Prepare payload
            payload = {
                "annual_revenue": annual_revenue,
                "expenses_total": expenses_total,
                "num_employees": num_employees,
                "avg_employee_salary": avg_employee_salary,
                "customer_growth_rate": customer_growth_rate,
                "customer_retention_rate": customer_retention_rate,
                "digital_spending_ratio": digital_spending_ratio,
                "profit_to_expense_ratio": profit_to_expense_ratio,
                "cash_flow_score": cash_flow_score,
                "credit_score": credit_score,
                "traction_score": traction_score,
                "bookkeeping_quality": bookkeeping_quality,
                "data_protection_score": data_protection_score,
                "financial_transparency_score": financial_transparency_score,
                "AML_risk_flag": int(AML_risk_flag),
                "has_pitch_deck": int(has_pitch_deck),
                "registered_business": int(registered_business),
                "female_owned": int(female_owned),
                "employee_contracts_verified": int(employee_contracts_verified),
                "years_in_operation": years_in_operation,
                "tech_adoption_level": tech_adoption_level,
                "sector": sector,
                "country": country,
                "region": region,
                "prior_investment": prior_investment,
                "tax_compliance_status": tax_compliance_status,
                "regulatory_license_status": regulatory_license_status,
                "remote_work_policy": remote_work_policy
            }
            
            # Show loading animation
            with st.spinner("🔮 AI is analyzing your business..."):
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.02)
                    progress_bar.progress(i + 1)
                
                try:
                    # Call API
                    response = requests.post(f"{API_BASE_URL}/predict/sme", json=payload, timeout=60)
                    
                    if response.status_code == 200:
                        results = response.json()
                        st.session_state.results = results
                        st.session_state.analysis_complete = True
                        
                        # Send to n8n
                        send_to_n8n({"timestamp": datetime.now().isoformat(), **payload, **results})
                        
                        st.markdown('<div class="success-message">✨ Analysis Complete! Your AI insights are ready.</div>', 
                                  unsafe_allow_html=True)
                    else:
                        st.error(f"❌ API Error: {response.status_code}")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        
        # Display Results
        if st.session_state.analysis_complete and st.session_state.results:
            results = st.session_state.results
            predictions = results.get("predictions", {})
            advice = results.get("overall_advice", "")
            
            # Personalized Greeting
            business_name = st.session_state.get('business_name', 'Your Business')
            owner_name = st.session_state.get('owner_name', 'there')
            
            st.markdown(f'''
                <div class="personalized-greeting">
                    <h2>🎉 Hello, {owner_name}!</h2>
                    <p>Here's your comprehensive AI analysis for <strong>{business_name}</strong></p>
                </div>
            ''', unsafe_allow_html=True)
            
            st.markdown('<h2 class="section-header">🎯 AI-Powered Insights</h2>', unsafe_allow_html=True)
            
            # Metrics Dashboard
            col_m1, col_m2, col_m3 = st.columns(3)
            with col_m1:
                st.markdown(f"""
                    <div class="metric-card">
                        <p class="metric-value">{predictions.get('funding', 0):.0f}</p>
                        <p class="metric-label">💰 Funding Score</p>
                    </div>
                """, unsafe_allow_html=True)
            with col_m2:
                st.markdown(f"""
                    <div class="metric-card">
                        <p class="metric-value">{predictions.get('compliance', 0):.0f}</p>
                        <p class="metric-label">⚖️ Compliance</p>
                    </div>
                """, unsafe_allow_html=True)
            with col_m3:
                st.markdown(f"""
                    <div class="metric-card">
                        <p class="metric-value">{predictions.get('growth', 0):.1f}%</p>
                        <p class="metric-label">📈 Growth</p>
                    </div>
                """, unsafe_allow_html=True)
            
            # Gauges
            st.markdown("<br>", unsafe_allow_html=True)
            col_g1, col_g2 = st.columns(2)
            with col_g1:
                st.plotly_chart(create_gauge_chart(predictions.get('funding', 0), "Funding Readiness"), 
                              use_container_width=True)
            with col_g2:
                st.plotly_chart(create_gauge_chart(predictions.get('compliance', 0), "Compliance Score"), 
                              use_container_width=True)
            
            # Radar Chart - Business Health
            radar_categories = ['Funding', 'Compliance', 'Growth', 'Tech', 'Market']
            radar_values = [
                predictions.get('funding', 0),
                predictions.get('compliance', 0),
                predictions.get('growth', 50),
                tech_adoption_level == "cutting_edge" and 90 or 60,
                traction_score
            ]
            st.plotly_chart(create_radar_chart(radar_categories, radar_values, "🎯 Business Health Radar"), 
                          use_container_width=True)
            
            # AI Advice - Enhanced Display
            st.markdown(f'''
                <div class="advice-section">
                    <h3>🤖 Personalized AI Advisory Report for {business_name}</h3>
                    <div style="background: white; padding: 1.5rem; border-radius: 15px; margin-top: 1rem; line-height: 1.8; color: #333;">
                        {format_advice_with_styling(advice)}
                    </div>
                </div>
            ''', unsafe_allow_html=True)
            
            # Action Buttons
            st.markdown("<br>", unsafe_allow_html=True)
            col_b1, col_b2, col_b3 = st.columns(3)
            with col_b1:
                if st.button("📢 Share to Slack", use_container_width=True):
                    business_name = st.session_state.get('business_name', 'Business')
                    slack_webhook_url = st.session_state.get('slack_webhook') or SLACK_WEBHOOK_URL
                    
                    slack_message = f"""🚀 *Inua360 Analysis Complete for {business_name}*

📊 *Key Metrics:*
• Funding Readiness: {predictions.get('funding', 0):.0f}/100
• Compliance Score: {predictions.get('compliance', 0):.0f}/100
• Growth Projection: {predictions.get('growth', 0):.1f}%

💡 Analysis generated for: {st.session_state.get('owner_name', 'Business Owner')}
🕒 {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
"""
                    if send_to_slack(slack_message, slack_webhook_url):
                        st.success("✅ Shared to Slack!")
                    else:
                        st.warning("⚠️ Please provide a valid Slack webhook URL in the form above")
            with col_b2:
                if st.button("🎙️ Listen to Summary", use_container_width=True):
                    generate_voice_summary(advice)
            with col_b3:
                if st.button("📊 Download Report", use_container_width=True):
                    report_data = json.dumps(results, indent=2)
                    st.download_button("⬇️ Download JSON", report_data, "inua360_report.json", "application/json")
        else:
            # Placeholder when no results
            st.markdown("""
                <div class="result-card" style="text-align: center; padding: 4rem 2rem;">
                    <h2 style="color: #FF6B35; font-size: 2.5rem;">🎯</h2>
                    <h3 style="color: #666;">Ready for AI-Powered Insights?</h3>
                    <p style="color: #999; margin-top: 1rem;">Fill in your business details and click <strong>RUN AI ANALYSIS</strong> to get started!</p>
                    <div style="margin-top: 2rem;">
                        <span class="badge badge-info">💰 Funding Predictions</span>
                        <span class="badge badge-success">⚖️ Compliance Analysis</span>
                        <span class="badge badge-warning">📈 Growth Forecasts</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div style="text-align: center; padding: 2rem; color: #999;">
            <p>Built for Kenyan SMEs | Powered by AI & Innovation</p>
            <p style="font-size: 0.9rem;">🚀 Inua360 © 2025 | <a href="https://elevateai-global.slack.com/" target="_blank" style="color: #FF6B35;">Join our Slack</a></p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
