INUA 360 – The Autonomous SME Co-Pilot for Kenya
“The AI that runs your entire back-office while you sell.”
2026 Production Release | Built for Kenyan SMEs | Zero admin. Zero stress.
┌──────────────────────────────────────────────────────────────────────┐
│  7.5 million Kenyan SMEs • 98 % informal • 70 % run out of cash     │
│  → Inua 360 wakes up every day and fixes it automatically           │
└──────────────────────────────────────────────────────────────────────┘
What Inua 360 Does (for the owner)

Connects your M-Pesa once → never enters a number again
Tells you exactly how much money you’ll have in 21 days
Renews licences, pays NSSF/NHIF, files KRA returns before you remember
Finds grants, loans, and tenders you actually qualify for
Fills and submits every form for you (one tap “Yes”)
All on WhatsApp (or Gmail/Slack/USSD if you prefer)

The 8 Autonomous Agents (the brain)


















































AgentJob (every day)Magic you see on WhatsApp / Web App1. ProfileBuilds your full business card automatically“I know you’re a retail duka in Kisumu, women-owned, KES 24M/year”2. FinancialsPulls & categorises every M-Pesa transactionLive river chart + “You made KES 84k yesterday”3. Cash-Flow21-day & 90-day forecast + gap alerts“You’ll be short KES 1.2M on 12 Dec — I’m fixing it”4. ComplianceTracks & renews every licence/permit“Your county licence expires in 11 days — shall I renew?”5. FundingFinds loans & grants you have 80–96 % chance“3 funding options ready — KIE KES 5M, NYOTA KES 3M — shall I apply?”6. TenderOnly alerts for tenders you can actually win“89 % fit tender – Nairobi furniture (women reserved) – shall I bid?”7. ApplicationFills & submits any form in Kenya“Application submitted! Here’s the screenshot and reference number”8. SupervisorThe brain that decides who acts & talks to youYou type anything → Inua understands instantly
Final Tech Stack (2026 Production)























































LayerTechnologyWhy it wins in KenyaFrontendNext.js 15 (App Router) + Tailwind + PWAWorks offline, 2G, instant load on cheap phonesBackend & APIFastAPI (Python) + PostgreSQL (Neon/Railway)Blazing fast, cheap, async, easy for Kenyan devsOrchestrationn8n (self-hosted or cloud)Visual workflows, no-code changes, beloved by teamsML InferenceLlama-3.1-8B / Mixtral / XGBoost / ProphetYou choose best model per task (liberty)DatabasePostgreSQL (Neon.tech or Railway)Free tier forever, serverless, real-timeWhatsAppMeta WhatsApp Business Cloud APIOfficial, unlimited messages, templatesForm AutomationPuppeteer/Playwright (headless)Works on 99 % of Kenyan government sitesHostingVercel (frontend) • Railway/Render (backend)Kenya edge nodes, KES 1–3k/month for 10k usersReal-time FeedWebSockets from n8nLive “Agent Activity” TikTok-style feed
Architecture Diagram (beautiful version)
→ https://files.catbox.moe/0q2r1l.png (dark)
→ https://files.catbox.moe/3c9q8v.png (light)
Folder Structure (monorepo)
textinua360/
├── backend/              → FastAPI + PostgreSQL models
├── ml-service/           → All 6 ML endpoints (Docker)
├── n8n/                  → All 8 agent workflows (import JSONs)
├── frontend/             → Next.js 15 web app + PWA
├── puppeteer/            → Application Agent scripts
├── docs/                 → Architecture, pitch deck, diagrams
└── README.md             ← you are here
Pricing (2026)

























TierPriceWhat you getFreeKES 0Profile + basic alertsProKES 990/monthFull compliance + funding notificationsAutonomousKES 2,900–4,900 + 3–8 % success feeAgents apply, track, manage everything
Current Status (November 2025)

Agents 1–3 (Profile, Financials, Cash-Flow) → 100 % ready JSON
Architecture final → no more changes
Backend + Frontend starter repos ready
Beta launch target: January 2026

Quick Start for Developers
Bash# 1. Backend + ML
git clone https://github.com/inua360/backend
cd backend && docker-compose up -d

# 2. Frontend
git clone https://github.com/inua360/frontend
cd frontend && npm run dev

# 3. n8n (import the 8 JSON files)
docker run -p 5678:5678 n8nio/n8n
→ Import workflows from n8n/ folder
The Team Dream
