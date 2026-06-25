# Draftly 🚀

AI-powered Gmail Assistant built using **FastAPI**, **PostgreSQL**, **OpenAI**, and the **Gmail API**.

Draftly allows users to securely authenticate with Gmail, fetch emails, generate AI-powered replies, manage drafts, and send responses directly from their Gmail account.

---

# Features ✨

## Authentication & Security

* Google OAuth 2.0 Authentication
* JWT Token Generation
* Multi-user Support
* Protected API Endpoints
* Automatic Gmail Token Refresh
* PKCE-based OAuth Flow

---

## Gmail Integration

* Fetch unread Gmail messages
* Read email details
* Extract sender, subject, and body
* Store emails in PostgreSQL
* Send replies directly through Gmail
* Refresh expired Gmail tokens automatically

---

## AI Features

* Generate professional email replies using OpenAI
* Friendly and context-aware responses
* Draft management workflow
* Editable AI-generated drafts

---

## Backend Features

* FastAPI REST APIs
* PostgreSQL Database
* SQLAlchemy ORM
* Alembic Database Migrations
* Centralized Logging
* Global Exception Handling
* Environment-based Configuration

---

# System Architecture

```text
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
```

---

# Tech Stack

## Backend

* Python 3.10+
* FastAPI
* SQLAlchemy
* Pydantic

## Authentication

* Google OAuth 2.0
* JWT Authentication

## AI

* OpenAI API

## Database

* PostgreSQL
* Neon PostgreSQL
* Alembic

## Deployment

* Render
* GitHub

---

# Database Design

## Users

| Column        | Type     |
| ------------- | -------- |
| id            | Integer  |
| email         | String   |
| access_token  | String   |
| refresh_token | String   |
| created_at    | DateTime |

---

## Emails

| Column           | Type     |
| ---------------- | -------- |
| id               | Integer  |
| gmail_message_id | String   |
| sender           | String   |
| subject          | String   |
| body             | Text     |
| category         | String   |
| priority         | String   |
| user_id          | Integer  |
| created_at       | DateTime |

---

## Drafts

| Column          | Type     |
| --------------- | -------- |
| id              | Integer  |
| user_id         | Integer  |
| email_id        | Integer  |
| generated_reply | Text     |
| edited_reply    | Text     |
| status          | String   |
| created_at      | DateTime |

---

# API Flow

## 1. Login with Gmail

```http
GET /auth/google/login
```

Redirects user to Google OAuth consent screen.

---

## 2. OAuth Callback

```http
GET /auth/google/callback
```

* Exchanges authorization code
* Stores Gmail tokens
* Generates JWT token

---

## 3. Fetch Emails

```http
GET /gmail/emails
```

Fetch unread emails from Gmail and store them in PostgreSQL.

---

## 4. Generate AI Draft

```http
POST /draft/generate/{email_id}
```

Generate an AI-powered email reply.

---

## 5. Send Reply

```http
POST /gmail/send/{draft_id}
```

Send the generated draft via Gmail.

---

# Project Structure

```text
app
├── core
│   ├── config.py
│   ├── database.py
│   ├── dependencies.py
│   └── security.py
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
├── alembic.ini
├── requirements.txt
└── README.md
```

---

# Logging

Centralized logging is implemented for:

* User Authentication
* Gmail OAuth
* Gmail Token Refresh
* Email Fetching
* Draft Generation
* Email Sending
* Error Tracking

---

# Exception Handling

Global exception handlers provide consistent API responses.

Example:

```json
{
  "success": false,
  "message": "Token refresh failed"
}
```

---

# Running Locally

## Clone Repository

```bash
git clone <repository-url>
cd Draftly
```

---

## Create Virtual Environment

```bash
python -m venv .venv
```

Activate:

Windows

```bash
.venv\Scripts\activate
```

Mac/Linux

```bash
source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file:

```env
DATABASE_URL=

SECRET_KEY=

GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=

OPENAI_API_KEY=
```

---

## Run Database Migrations

```bash
alembic upgrade head
```

---

## Start FastAPI

```bash
uvicorn app.main:app --reload
```

---

## Swagger Documentation

```text
http://localhost:8001/docs
```

---

# Deployment

Production deployment is hosted on:

* Render
* Neon PostgreSQL

Environment variables are configured directly in Render.

https://draftly-jtgt.onrender.com/


---

# Future Enhancements

* Email Categorization
* Priority Detection
* Background Tasks
* Redis Caching
* Celery Workers
* Dashboard Analytics
* Email Search
* User Settings & Preferences

---

# Key Learnings

This project demonstrates:

* FastAPI Development
* REST API Design
* Google OAuth 2.0
* JWT Authentication
* OpenAI Integration
* Gmail API Integration
* PostgreSQL Design
* SQLAlchemy ORM
* Alembic Migrations
* Render Deployment
* Logging & Exception Handling
* Multi-user Backend Development

```
```
