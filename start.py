"""
🚀 Inua360 SME AI Agent - Quick Start Script
Launches both API server and Streamlit dashboard automatically
"""

import subprocess
import sys
import time
import os
from pathlib import Path

def check_env_files():
    """Check and create environment files if they don't exist"""
    project_root = Path(__file__).parent
    
    # Check .env file
    env_file = project_root / ".env"
    if not env_file.exists():
        print("⚠️  Warning: .env file not found!")
        print("Creating template .env file...")
        env_file.write_text(
            "OPENAI_API_KEY=your_openai_api_key_here\n"
            "PORT=8000\n"
        )
        print("✅ Created .env file. Please add your OpenAI API key!")
        print()
    
    # Check secrets.toml
    secrets_dir = project_root / ".streamlit"
    secrets_file = secrets_dir / "secrets.toml"
    
    if not secrets_file.exists():
        print("⚠️  Warning: .streamlit/secrets.toml not found!")
        print("Creating .streamlit directory and template secrets file...")
        secrets_dir.mkdir(exist_ok=True)
        secrets_file.write_text(
            '# API Configuration\n'
            'API_BASE_URL = "http://localhost:8000"\n'
            'N8N_WEBHOOK_URL = "https://abby218.app.n8n.cloud/webhook/sme-data"\n'
            '\n'
            '# Slack Integration\n'
            'SLACK_WEBHOOK_URL = "your_slack_webhook_here"\n'
            '\n'
            '# ElevenLabs Voice API\n'
            'ELEVENLABS_API_KEY = "your_elevenlabs_key_here"\n'
            'ELEVENLABS_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"\n'
        )
        print("✅ Created .streamlit/secrets.toml. Please configure your API keys!")
        print()

def main():
    print("=" * 60)
    print("🚀 Inua360 SME AI Agent - Startup Script")
    print("=" * 60)
    print()
    
    # Check environment files
    check_env_files()
    
    print("Select startup option:")
    print("1. Run Streamlit Dashboard only (connect to deployed API)")
    print("2. Run both API Server and Dashboard (local development)")
    print("3. Run API Server only")
    print()
    
    try:
        choice = input("Enter choice (1-3): ").strip()
    except KeyboardInterrupt:
        print("\n\nStartup cancelled.")
        sys.exit(0)
    
    if choice == "1":
        print()
        print("🎨 Starting Streamlit Dashboard...")
        print("Dashboard will use deployed API at: https://inua360-the-kenyan-sme-ai-agent.onrender.com")
        print()
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    
    elif choice == "2":
        print()
        print("🔧 Starting API Server and Dashboard...")
        print()
        
        # Start API server in background
        print("Starting FastAPI server...")
        api_process = subprocess.Popen(
            [sys.executable, "inua360_the_kenyan_sme_ai_agent/modeling/predictions_api.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        print("Waiting 5 seconds for API to start...")
        time.sleep(5)
        
        print("API Server running at: http://localhost:8000")
        print("API Docs at: http://localhost:8000/docs")
        print()
        print("Starting Streamlit Dashboard...")
        
        try:
            subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
        except KeyboardInterrupt:
            print("\n\nShutting down services...")
        finally:
            api_process.terminate()
            api_process.wait()
            print("✅ All services stopped.")
    
    elif choice == "3":
        print()
        print("🔧 Starting API Server only...")
        print("API will be available at: http://localhost:8000")
        print("API Docs at: http://localhost:8000/docs")
        print()
        subprocess.run([
            sys.executable, 
            "inua360_the_kenyan_sme_ai_agent/modeling/predictions_api.py"
        ])
    
    else:
        print("❌ Invalid choice! Please run again and select 1, 2, or 3.")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✅ Startup cancelled. Goodbye!")
        sys.exit(0)
