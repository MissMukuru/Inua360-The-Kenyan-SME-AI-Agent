@echo off
echo ============================================
echo 🚀 Inua360 SME AI Agent - Startup Script
echo ============================================
echo.

REM Check if .env file exists
if not exist .env (
    echo ⚠️  Warning: .env file not found!
    echo Creating template .env file...
    (
        echo OPENAI_API_KEY=your_openai_api_key_here
        echo PORT=8000
    ) > .env
    echo ✅ Created .env file. Please add your OpenAI API key!
    echo.
)

REM Check if .streamlit\secrets.toml exists
if not exist .streamlit\secrets.toml (
    echo ⚠️  Warning: .streamlit\secrets.toml not found!
    echo Creating .streamlit directory and template secrets file...
    mkdir .streamlit 2>nul
    (
        echo # API Configuration
        echo API_BASE_URL = "http://localhost:8000"
        echo N8N_WEBHOOK_URL = "https://abby218.app.n8n.cloud/webhook/sme-data"
        echo.
        echo # Slack Integration
        echo SLACK_WEBHOOK_URL = "your_slack_webhook_here"
        echo.
        echo # ElevenLabs Voice API
        echo ELEVENLABS_API_KEY = "your_elevenlabs_key_here"
        echo ELEVENLABS_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"
    ) > .streamlit\secrets.toml
    echo ✅ Created .streamlit\secrets.toml. Please configure your API keys!
    echo.
)

echo Select startup option:
echo 1. Run Streamlit Dashboard only (connect to deployed API)
echo 2. Run both API Server and Dashboard (local development)
echo 3. Run API Server only
echo.
set /p choice="Enter choice (1-3): "

if "%choice%"=="1" (
    echo.
    echo 🎨 Starting Streamlit Dashboard...
    echo Dashboard will use deployed API at: https://inua360-the-kenyan-sme-ai-agent.onrender.com
    echo.
    streamlit run app.py
) else if "%choice%"=="2" (
    echo.
    echo 🔧 Starting API Server and Dashboard...
    echo.
    echo Starting FastAPI server in new window...
    start "Inua360 API Server" cmd /k "python inua360_the_kenyan_sme_ai_agent\modeling\predictions_api.py"
    
    echo Waiting 5 seconds for API to start...
    timeout /t 5 /nobreak >nul
    
    echo Starting Streamlit Dashboard...
    streamlit run app.py
) else if "%choice%"=="3" (
    echo.
    echo 🔧 Starting API Server only...
    echo API will be available at: http://localhost:8000
    echo API Docs at: http://localhost:8000/docs
    echo.
    python inua360_the_kenyan_sme_ai_agent\modeling\predictions_api.py
) else (
    echo Invalid choice! Please run again and select 1, 2, or 3.
    pause
    exit /b
)

pause
