# Draftly 🚀

Draftly is an AI-powered Gmail automation backend built using FastAPI, PostgreSQL, Gmail API, and OpenAI.

It helps users:

- Authenticate securely with Gmail using Google OAuth
- Fetch unread Gmail emails
- Store emails in PostgreSQL
- Generate intelligent AI-powered replies
- Save AI-generated drafts
- Send emails directly through Gmail API
- Automatically mark processed emails as read

---

# Features ✨

## Gmail Integration
- Google OAuth 2.0 authentication
- Gmail API integration
- Fetch unread emails
- Send emails directly from Gmail
- Automatically mark processed emails as read

## AI Automation
- AI-generated professional email replies
- Multiple response tones
  - Formal
  - Friendly
  - Concise
  - Corporate
- OpenAI GPT integration (`gpt-4.1-mini`)
- Smart prompt engineering

## Database Features
- PostgreSQL integration
- Store fetched emails
- Store generated drafts
- Avoid duplicate email storage
- Persistent user OAuth tokens

## Backend Architecture
- FastAPI modular architecture
- SQLAlchemy ORM
- Service-based structure
- Dependency injection
- REST API endpoints
- Swagger API documentation

---

# Tech Stack 🛠️

## Backend
- FastAPI
- Python
- SQLAlchemy
- PostgreSQL

## AI
- OpenAI API (`gpt-4.1-mini`)

## Authentication & Email
- Google OAuth 2.0
- Gmail API

## Tools & Utilities
- Uvicorn
- Pydantic
- python-dotenv

---

# System Workflow 🔄

```text
Google OAuth Login
        ↓
Fetch Unread Emails
        ↓
Store Emails in PostgreSQL
        ↓
Generate AI Replies
        ↓
Save Drafts
        ↓
Mark Emails as Read
        ↓
Send Emails via Gmail API
Project Structure 📁
Draftly/
│
├── app/
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── email.py
│   │   └── draft.py
│   │
│   ├── routes/
│   │   ├── auth_routes.py
│   │   ├── gmail_routes.py
│   │   └── draft_routes.py
│   │
│   ├── services/
│   │   ├── gmail_service.py
│   │   └── ai_service.py
│   │
│   ├── utils/
│   │   └── dependencies.py
│   │
│   ├── database.py
│   └── main.py
│
├── .env
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── credentials.json
└── README.md
Installation ⚙️
1. Clone Repository
git clone <your-repository-url>
cd Draftly
2. Create Virtual Environment
Windows
python -m venv .venv
.\.venv\Scripts\activate
Mac/Linux
python3 -m venv .venv
source .venv/bin/activate
3. Install Dependencies
pip install -r requirements.txt
Environment Variables 🔐

Create a .env file in the project root directory.

DATABASE_URL=postgresql://postgres:password@localhost:5432/draftly

OPENAI_API_KEY=your_openai_api_key

GOOGLE_CLIENT_ID=your_google_client_id

GOOGLE_CLIENT_SECRET=your_google_client_secret

SECRET_KEY=your_secret_key
PostgreSQL Setup 🐘
Create Database
CREATE DATABASE draftly;
Google OAuth Setup 🔑
1. Go to Google Cloud Console

Enable:

Gmail API
2. Create OAuth Credentials

Create:

OAuth Client ID
3. Add Redirect URI
http://localhost:8001/auth/callback
4. Download Credentials

Download OAuth credentials JSON file and rename it to:

credentials.json

Place it in project root directory.

Run the Application ▶️
uvicorn app.main:app --reload --port 8001

Application runs on:

http://127.0.0.1:8001
API Documentation 📚

Swagger UI:

http://127.0.0.1:8001/docs
API Endpoints 🌐
Authentication
Method	Endpoint	Description
GET	/auth/login	Gmail OAuth login
GET	/auth/callback	OAuth callback
Gmail APIs
Method	Endpoint	Description
GET	/gmail/emails	Fetch unread emails
POST	/gmail/send/{draft_id}	Send generated draft
AI Draft Generation
Method	Endpoint	Description
POST	/draft/generate/{email_id}	Generate AI email reply
Tone Support

Example:

/draft/generate/1?tone=friendly

Supported tones:

formal
friendly
concise
corporate
Sample AI Response 🤖
{
  "reply": "Dear Hiring Team,\n\nThank you for reaching out regarding the interview opportunity. I would be happy to connect next week and discuss further.\n\nBest regards,\nNikita"
}
Database Models 🗄️
User

Stores:

Gmail account
OAuth access token
Refresh token
Email

Stores:

Gmail message ID
Sender
Subject
Email body
Draft

Stores:

AI-generated reply
Draft status
Duplicate Email Prevention ✅

Draftly avoids storing duplicate Gmail messages by checking:

gmail_message_id

before insertion into database.

Email Lifecycle 📬
Unread Email
      ↓
Fetched from Gmail
      ↓
Stored in Database
      ↓
AI Reply Generated
      ↓
Marked as Read
      ↓
Draft Sent
Run with Docker 🐳
Build Containers
docker-compose up --build
Stop Containers
docker-compose down
Future Improvements 🚧
React frontend dashboard
Streamlit UI
JWT authentication
Multi-user support
Background task scheduling
Celery integration
Gmail thread support
AI reply approval workflow
Email categorization
RAG-based email context memory
Deployment on AWS / Render / Railway
Security Notes 🔒

Never commit:

.env
credentials.json
OAuth tokens
API keys

Add these to .gitignore:

.env
.venv/
__pycache__/
credentials.json
Learning Outcomes 📘

This project demonstrates practical implementation of:

FastAPI
REST APIs
Gmail API
Google OAuth 2.0
OpenAI API
SQLAlchemy ORM
PostgreSQL
AI automation workflows
Token refresh handling
Backend architecture design
Author 👩‍💻

Built with ❤️ using FastAPI, Gmail API, PostgreSQL, and OpenAI.