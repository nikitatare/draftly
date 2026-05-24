from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.email import Email
import os
from app.utils.dependencies import get_db
from app.models.user import User
from app.services.gmail_service import (
    get_gmail_service,
    fetch_unread_emails,
    get_email_detail,
    parse_email_data
)

from google.oauth2.credentials import Credentials
from app.models.draft import Draft
from app.services.gmail_service import send_email, get_gmail_service

router = APIRouter()

@router.get("/emails")
def get_emails(db: Session = Depends(get_db)):
    user = db.query(User).first()
    credentials = Credentials(
        token=user.access_token,
        refresh_token=user.refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET")
    )

    service = get_gmail_service(credentials)

    emails = fetch_unread_emails(service)

    saved_emails = []
    for msg in emails:

        existing = db.query(Email).filter(
            Email.gmail_message_id == msg["id"]
        ).first()

        # Skip if already stored
        if existing:
            continue

        detail = get_email_detail(
            service,
            msg["id"]
        )

        # Save into DB
        parsed_email = parse_email_data(detail)

        email = Email(
            gmail_message_id=msg["id"],
            sender=parsed_email["sender"],
            subject=parsed_email["subject"],
            body=parsed_email["body"]
        )
        db.add(email)

        saved_emails.append({
            "gmail_message_id": msg["id"]
        })

    db.commit()

    return {
        "message": "Emails fetched and stored",
        "emails": saved_emails
    }

@router.post("/send/{draft_id}")
def send_draft(
    draft_id: int,
    db: Session = Depends(get_db)
):

    user = db.query(User).first()

    credentials = Credentials(
        token=user.access_token,
        refresh_token=user.refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET")
    )

    service = get_gmail_service(credentials)

    draft = db.query(Draft).filter(
        Draft.id == draft_id
    ).first()

    send_email(
        service,
        "nikitaprakashtare@gmail.com",
        "AI Reply",
        draft.generated_reply
    )

    draft.status = "sent"

    db.commit()

    return {
        "message": "Email sent"
    }