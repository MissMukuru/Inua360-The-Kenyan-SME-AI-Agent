# Inua 360 – The Autonomous SME Co-Pilot for Kenya

**The AI that runs your entire back-office while you sell**  
2026 Production Release • Built for Kenyan SMEs • Zero admin, maximum growth

![Inua 360](https://files.catbox.moe/3c9q8v.png)

[![Made in Kenya](https://img.shields.io/badge/Made_in-Kenya-FA6915?style=flat&logo=kenya)](https://kenya.co.ke)
[![Next.js](https://img.shields.io/badge/Next.js_15-000000?logo=next.js&logoColor=white)](https://nextjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![n8n](https://img.shields.io/badge/n8n-FF6D00?logo=n8n&logoColor=white)](https://n8n.io)

## What Inua 360 Does for the Owner

| Feature                    | What you experience every day                                            |
|----------------------------|--------------------------------------------------------------------------|
| M-Pesa Auto-Sync           | Connect once → never type a transaction again                            |
| Live Money Hub             | “KES 1.8M in pockets today – last synced 2 mins ago”                     |
| 21-Day Forecast            | “You’ll have KES 680k surplus” or “Short KES 1.2M on 12 Dec – fixing it” |
| Compliance Shield          | “Your licence expires in 11 days — shall I renew?”                      |
| Funding Radar              | “3 funding options you have 91–96 % chance to get — shall I apply?”      |
| Tender Sniper              | “89 % fit tender – women reserved – shall I bid?”                        |
| One-Tap Applications       | Tap “Yes” → Inua fills & submits any form in Kenya                      |
| Daily WhatsApp Summary     | 95 % of usage happens here                                               |

## The 8 Autonomous Agents

| # | Agent              | Daily Job                                          | ML Model (choose best)                          |
|---|--------------------|----------------------------------------------------|-------------------------------------------------|
| 1 | Profile Agent      | Builds your full business card automatically       | Llama-3.1-8B / Mixtral / Claude                 |
| 2 | Financials Agent   | Pulls & categorises every M-Pesa transaction       | Llama-3.1 fine-tuned / BERT-Kiswahili           |
| 3 | Cash-Flow Agent    | 21 & 90-day forecasts + gap alerts                 | Prophet + LSTM / Temporal Fusion Transformer    |
| 4 | Compliance Agent   | Tracks & renews licences, KRA, NSSF, NHIF          | XGBoost / LightGBM                              |
| 5 | Funding Agent      | Finds grants/loans you actually qualify for        | sentence-transformers (MiniLM fine-tuned)       |
| 6 | Tender Agent       | Only alerts for tenders you can win (≥75 % fit)    | XGBoost (15k past awards)                       |
| 7 | Application Agent  | Fills & submits any form in Kenya                  | Puppeteer/Playwright + OCR                      |
| 8 | Supervisor Agent   | Decides who acts & talks to you naturally          | Llama-3.1-8B / Grok / Mistral-7B                |

## Final Tech Stack (2026 Production)

| Layer             | Technology                               | Hosting                     | Cost (10k users) |
|-------------------|------------------------------------------|-----------------------------|------------------|
| Frontend          | Next.js 15 + Tailwind + PWA              | Vercel (Nairobi edge)       | Free – KES 2k    |
| Backend & API     | FastAPI (Python 3.12) + PostgreSQL       | Railway / Render            | KES 3–5k         |
| Orchestration     | n8n (self-hosted or cloud)               | Railway / Hetzner           | KES 2–4k         |
| ML Inference      | Llama-3.1-8B / Mixtral / XGBoost         | Groq / Together.ai / local  | KES 8–15k        |
| Database          | PostgreSQL (Neon.tech or Railway)        | Serverless                  | Free tier        |
| WhatsApp          | Meta WhatsApp Business Cloud API         | Official                    | Free (templates) |
| Form Automation   | Puppeteer/Playwright (headless)          | Railway container           | KES 1k           |
| Real-time Feed    | WebSocket from n8n                       | Built-in                    | Free             |

## Architecture Diagram

![Architecture](https://files.catbox.moe/0q2r1l.png)

## Project Structure (Monorepo)

```bash
inua360/
├── backend/          # FastAPI + PostgreSQL models
├── ml-service/       # 6 ML endpoints (Docker)
├── n8n/              # 8 agent workflows (ready JSONs)
├── frontend/         # Next.js 15 + PWA
├── puppeteer/        # Application Agent scripts
├── docs/             # Diagrams, pitch deck
└── README.md         # ← you are here

Quick Start
# Backend + ML
git clone https://github.com/inua360/backend && cd backend
docker-compose up -d

# Frontend
git clone https://github.com/inua360/frontend && cd frontend
npm install && npm run dev

# n8n
docker run -p 5678:5678 n8nio/n8n
# → Import workflows from n8n/ folder
