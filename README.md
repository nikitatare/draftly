# Draftly 🚀

Draftly is an AI-powered email assistant built using FastAPI, PostgreSQL, Gmail API, and OpenAI.

It helps users:
- Authenticate with Gmail
- Fetch emails
- Generate professional AI email replies
- Save drafts
- Send responses automatically

---

# Features ✨

- Gmail OAuth Authentication
- Fetch unread Gmail messages
- AI-generated professional email replies
- PostgreSQL database integration
- FastAPI backend architecture
- Swagger API documentation
- Modular service-based structure
- OpenAI GPT integration

---

# Tech Stack 🛠️

## Backend
- FastAPI
- Python
- SQLAlchemy
- PostgreSQL

## AI
- OpenAI API (`gpt-4.1-mini`)

## Authentication
- Google OAuth 2.0
- Gmail API

---

# Project Structure 📁

```bash
Draftly/
│
├── app/
│   ├── routes/
│   │   ├── auth_routes.py
│   │   ├── gmail_routes.py
│   │   └── draft_routes.py
│   │
│   ├── services/
│   │   ├── ai_service.py
│   │   └── gmail_service.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── email.py
│   │   └── draft.py
│   │
│   ├── database.py
│   └── main.py
│
├── .env
├── requirements.txt
├── credentials.json
└── README.md
```

---

# Installation ⚙️

## 1. Clone Repository

```bash
git clone <your-repository-url>
cd Draftly
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

### Mac/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables 🔐

Create a `.env` file in the root directory.

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/draftly

OPENAI_API_KEY=your_openai_api_key

GOOGLE_CLIENT_ID=your_google_client_id

GOOGLE_CLIENT_SECRET=your_google_client_secret

SECRET_KEY=your_secret_key
```

---

# PostgreSQL Setup 🐘

## Create Database

```sql
CREATE DATABASE draftly;
```

---

# Run the Application ▶️

```bash
python -m uvicorn app.main:app --reload --port 8001
```

Server will run on:

```bash
http://127.0.0.1:8001
```

---

# API Documentation 📚

Swagger Docs:

```bash
http://127.0.0.1:8001/docs
```

---

# API Endpoints 🌐

## Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/auth/login` | Gmail OAuth login |
| GET | `/auth/callback` | OAuth callback |

---

## Gmail

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/gmail/emails` | Fetch unread emails |

---

## AI Draft Generation

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/draft/generate` | Generate AI email reply |

---

# Sample AI Response 🤖

```json
{
  "generated_reply": "Thank you for your email. I am available next week..."
}
```

---

# Future Improvements 🚧

- Frontend using React
- Real Gmail inbox integration
- Save generated drafts to database
- One-click email sending
- Tone customization
- Docker support
- JWT Authentication
- Background task scheduling
- Deployment on AWS/Render/Railway

---

# Security Notes 🔒

Never commit:
- `.env`
- `credentials.json`
- API keys
- OAuth secrets

Add these to `.gitignore`:

```gitignore
.env
.venv/
__pycache__/
credentials.json
```

---

# Author 👩‍💻

Built with ❤️ using FastAPI and OpenAI.