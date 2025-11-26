+-----------------------------------------------------------+
|                        USER                               |
|  WhatsApp / Gmail / Slack / USSD                          |
+-----------------------------------------------------------+
                     ↓ (inbound messages)
+-----------------------------------------------------------+
|             WhatsApp Business Cloud API                   |
+-----------------------------------------------------------+
                     ↓
+-----------------------------------------------------------+
|               SUPERVISOR AGENT (n8n)                      |
|   - Intent detection (LLM)                                |
|   - Routes to correct specialist                          |
+-----------------------------------------------------------+
        ↓           ↓           ↓           ↓           ↓
+--------+   +------------+   +----------+   +----------+   +----------+
|Profile |   |Financials  |   |Cash-Flow |   |Compliance|   |Funding   |
|Agent   |   |Agent       |   |Agent     |   |Agent     |   |Agent     |
+--------+   +------------+   +----------+   +----------+   +----------+
        ↓           ↓           ↓           ↓           ↓
+-----------------------------------------------------------+
|               SPECIALIST AGENTS (n8n workflows)           |
| 1–7 run on cron + webhooks                                |
+-----------------------------------------------------------+
                     ↓ (all call)
+-----------------------------------------------------------+
|               FastAPI ML Microservices                    |
| - extract-profile (Llama-3.1)                             |
| - categorise-txn (Llama-3.1)                               |
| - forecast-cashflow (Prophet+LSTM)                        |
| - compliance-score (XGBoost)                              |
| - funding-fit (sentence-transformers)                     |
| - tender-fit (XGBoost)                                    |
+-----------------------------------------------------------+
                     ↓
+-----------------------------------------------------------+
|                     Supabase                              |
| - profiles, transactions, forecasts,                      |
|   agent_log, documents, user_settings                     |
+-----------------------------------------------------------+
                     ↑
+-----------------------------------------------------------+
|              EXTERNAL SOURCES (scraped/pulled)           |
| M-Pesa Daraja | eCitizen | PPIP | 47 County Portals       |
| KRA iTax | NSSF/NHIF | IFMIS | Hustler/NYOTA/KIE         |
+-----------------------------------------------------------+
                     ↓
+-----------------------------------------------------------+
|             APPLICATION AGENT (Puppeteer)                 |
|   → Fills & submits any form automatically                |
+-----------------------------------------------------------+
                     ↓
                     USER GETS:
         WhatsApp reply + Web App (Next.js) + PDF reports
