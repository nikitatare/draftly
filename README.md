Draftly 🚀

AI-powered Gmail Assistant built with FastAPI, PostgreSQL, OpenAI, and Gmail API.

Draftly helps users authenticate with Gmail, fetch unread emails, generate AI-powered replies, create drafts, and send responses directly from their Gmail account.

Features ✨
Authentication & Security
Google OAuth 2.0 Login
JWT Authentication
Multi-user Support
Protected API Endpoints
Automatic Gmail Token Refresh
Gmail Integration
Fetch unread Gmail messages
Read email details
Extract sender, subject, and body
Mark emails as read after processing
Send replies directly from Gmail
AI Features
Generate professional email replies using OpenAI
Friendly response tone generation
Draft management workflow
Backend Features
FastAPI REST APIs
PostgreSQL Database
SQLAlchemy ORM
Alembic Database Migrations
Dockerized Deployment
Centralized Logging
Global Exception Handling
Architecture
                    +----------------+
                    | Google OAuth   |
                    +--------+-------+
                             |
                             v
+---------+        +------------------+
|  User   | -----> | FastAPI Backend  |
+---------+        +--------+---------+
                           |
         +-----------------+-----------------+
         |                                   |
         v                                   v
+------------------+              +----------------+
| Gmail API        |              | OpenAI API     |
| Fetch Emails     |              | Generate Reply |
| Send Emails      |              +----------------+
+------------------+
         |
         v
+------------------+
| PostgreSQL DB    |
| Users            |
| Emails           |
| Drafts           |
+------------------+
Tech Stack
Backend
Python 3.10
FastAPI
SQLAlchemy
PostgreSQL
Authentication
Google OAuth 2.0
JWT
AI
OpenAI API
Database
PostgreSQL
Alembic
DevOps
Docker
Docker Compose
Database Design
Users
id
email
access_token
refresh_token
created_at
Emails
id
gmail_message_id
sender
subject
body
user_id
Drafts
id
email_id
user_id
generated_reply
status
API Flow
1. Login
GET /auth/google/login

User authenticates with Google.

2. Generate JWT
GET /auth/google/callback

Draftly generates a JWT after successful Google authentication.

3. Fetch Emails
GET /gmail/emails

Fetch unread emails from Gmail and store them in PostgreSQL.

4. Generate Draft
POST /draft/generate/{email_id}

Generate AI-powered email reply.

5. Send Email
POST /gmail/send/{draft_id}

Send generated draft through Gmail.

Project Structure
app
├── core
│   ├── dependencies.py
│   ├── security.py
│
├── models
│   ├── user.py
│   ├── email.py
│   └── draft.py
│
├── routes
│   ├── auth_routes.py
│   ├── gmail_routes.py
│   └── draft_routes.py
│
├── services
│   ├── gmail_service.py
│   ├── ai_service.py
│   └── google_auth_service.py
│
├── utils
│   └── logger.py
│
├── alembic
│
├── Dockerfile
├── docker-compose.yml
└── README.md
Logging

Centralized logging implemented for:

User Authentication
Gmail Token Refresh
Email Fetching
Draft Generation
Email Sending
Error Tracking
Exception Handling

Global exception handling implemented using FastAPI exception handlers.

Examples:

{
  "success": false,
  "message": "Token refresh failed"
}
Running Locally
Clone Repository
git clone <repo-url>
cd Draftly
Install Dependencies
pip install -r requirements.txt
Environment Variables

Create .env

DATABASE_URL=
SECRET_KEY=

GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=

OPENAI_API_KEY=
Run Application
uvicorn app.main:app --reload
Docker Setup
docker-compose up --build
Future Enhancements
HTML Email Parsing
Email Categorization
Email Priority Detection
Background Jobs using Celery
Redis Integration
Dashboard Analytics
AWS Deployment
Key Learnings

This project demonstrates:

OAuth Authentication
JWT Security
REST API Development
Database Design
Dockerization
Database Migrations
OpenAI Integration
Gmail API Integration
Logging & Exception Handling
Multi-user Backend Development