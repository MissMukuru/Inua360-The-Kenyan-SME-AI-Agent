# Inua360 — The Kenyan SME AI Agent (Backend)

This repository contains the Django backend for Inua360 — an AI assistant targeted at Kenyan small and medium enterprises (SMEs). The backend provides REST APIs, models, and business logic that power the SME agent.

## Contents

- `manage.py` — Django project management script
- `db.sqlite3` — SQLite database (local development)
- `inua360/` — Django project configuration (settings, urls, wsgi, asgi)
- `sme/` — Django app for SME models, views, serializers, and routes

## Visual Project Overview

Below is a simple diagram showing the main components and how they interact:

```
   [Client: Web / Mobile] 
             |
             |  HTTP (REST)
             v
      [Django Backend (inua360 project)]
             |
   +---------+----------+
   |                    |
 [sme app]         [Other apps / services]
   |                    |
   v                    v
 [Models/Serializers]  [External Integrations]
   |                    |
   v                    v
 [SQLite (dev) / RDBMS (prod)]
```

The backend exposes API endpoints (see `sme/urls.py`) which are implemented in `sme/views.py` and serialized via `sme/serializers.py`. The Django settings are in `inua360/settings.py`.

## Quick setup (Windows / PowerShell)

These instructions assume you have Git and Python 3.11+ installed. Adjust the Python version and virtual environment tool if you prefer `venv`, `virtualenv`, or `conda`.

1. Clone the repository:

```powershell
git clone https://github.com/kelvinmaina01/Inua360-The-Kenyan-SME-AI-Agent.git
cd Inua360-The-Kenyan-SME-AI-Agent
git checkout backend
```

2. Create and activate a virtual environment (using venv):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If you see an execution policy error when activating the virtual environment on PowerShell, run (as Administrator):

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

3. Install Python dependencies:

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

4. Apply migrations and create a local superuser (development):

```powershell
python manage.py migrate
python manage.py createsuperuser
```

5. Run the development server:

```powershell
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser. API routes for the `sme` app are available under the paths defined in `sme/urls.py`.

## Common tasks

- Run tests:

```powershell
python manage.py test
```

- Run the Django shell:

```powershell
python manage.py shell
```

## Environment & Production notes

- For production use, switch from `SQLite` to a production-ready database such as PostgreSQL. Update `inua360/settings.py` to read database credentials from environment variables.
- Serve the Django app with a WSGI server (e.g., Gunicorn) behind a reverse proxy (Nginx). On Windows, consider using IIS or hosting on a Linux server/container for production.
- Keep secrets out of version control. Use environment variables or a secrets manager for `SECRET_KEY`, database passwords, and third-party API keys.

## Project contract (quick)

- Inputs: HTTP requests to REST endpoints (JSON payloads)
- Outputs: JSON responses, DB records
- Error modes: validation errors (400), authentication/permission errors (401/403), server errors (500)

## Where to look next

- `sme/models.py` — data models for SME profiles
- `sme/serializers.py` — serializers used by the API
- `sme/views.py` and `sme/urls.py` — view logic and routing
- `inua360/settings.py` — project configuration

## Troubleshooting

- If migrations fail, remove `db.sqlite3` (only for development) and re-run `python manage.py migrate`.
- If ports are in use, run `python manage.py runserver 0.0.0.0:8001` or choose another port.

## Contributing

If you'd like to contribute, please open an issue or a pull request against the `backend` branch. Include tests for new features and run `python manage.py test` before submitting.

---
Generated README for local development. If you want, I can also:

- Add a top-level `README.md` (project root) with a short summary and link to this backend README.
- Add a `Makefile` or PowerShell `scripts` folder to simplify common tasks.

If you'd like any changes to wording or additional sections (Docker, CI/CD, example API calls), tell me which and I'll add them.
