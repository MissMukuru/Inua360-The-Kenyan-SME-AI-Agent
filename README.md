
🖥️ Inua360 Frontend — SME AI Growth Platform

Welcome to the Frontend repository of Inua360 — an intelligent AI-powered platform designed to empower Kenyan SMEs by simplifying tender discovery, compliance, and financial management.

This branch focuses on building a fast, accessible, and user-friendly interface to help SMEs interact seamlessly with Inua360’s AI agents through the web.


---

✨ Key Features

📊 Tender Dashboard – Displays matched tender opportunities with eligibility and deadline summaries.

📝 Compliance & Readiness Interface – Shows document status, readiness score, and reminders.

💵 Finance Visualization – Interactive cashflow and loan-readiness visualization.

💬 Conversational Interface (Web) – Chat UI to interact with Inua360 agents for opportunity queries and status updates.

🧭 Responsive Design – Mobile-first experience to ensure accessibility for all SME users.

---

🧰 Tech Stack

Framework: React.js

UI Components: Tailwind CSS + ShadCN UI

Charts & Visualization: Recharts

State Management: Redux Toolkit

Routing: React Router

Authentication: Firebase Auth (planned)

Deployment: Vercel / Netlify

---

🚀 Getting Started

1. Clone the Repository

git clone https://github.com/TeamVunaAI/inua360.git
cd inua360/frontend

2. Install Dependencies

npm install

3. Start Development Server

npm run dev

> The app will run at http://localhost:5173 by default.

---

🏗️ Project Structure

frontend/
├── src/
│   ├── components/     # Reusable UI components
│   ├── pages/          # Page-level components
│   ├── layouts/        # Main layout and navigation
│   ├── store/          # Redux store & slices
│   ├── assets/         # Images & icons
│   └── utils/          # Helper functions
├── public/             # Static assets
├── package.json
└── vite.config.js

---

🔐 Environment Variables

Create a .env file in the frontend directory and add:

VITE_API_BASE_URL=https://your-backend-url/api
VITE_FIREBASE_API_KEY=your_key_here
VITE_FIREBASE_AUTH_DOMAIN=your_auth_domain

> ⚠️ Never commit your .env file to version control.

---

🧪 Testing & Linting

Run the following commands:

# Lint the project
npm run lint

# Run tests (if configured)
npm run test

---

📦 Build for Production

npm run build

The optimized build will be available in the dist/ directory.

---

🛠️ Future Enhancements

Integration with WhatsApp chatbot UI

Real-time notifications for tender opportunities

Role-based SME dashboards

Offline-first support (PWA)

---

🤝 Contributing

We welcome contributions!

1. Fork the repo


2. Create a feature branch (git checkout -b feature/your-feature)


3. Commit your changes (git commit -m "Add feature")


4. Push to your branch (git push origin feature/your-feature)


5. Open a Pull Request

---

👥 Frontend Contributors – Team VunaAI

---

📄 License

This frontend is released under the MIT License.
Feel free to fork, adapt, and build upon it.

---

✅ Inua360 — Empowering SMEs through AI.
“Find it. Finance it. Fulfill it.”

---


