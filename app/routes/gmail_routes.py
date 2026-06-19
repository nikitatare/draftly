from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.email import Email
import os
from app.core.dependencies import get_db
from app.models.user import User
from app.services.gmail_service import (
    fetch_unread_emails,
    get_email_detail,
    parse_email_data
)
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from app.core.dependencies import get_current_user
from app.models.draft import Draft
from app.services.gmail_service import send_email, get_gmail_service, extract_email

router = APIRouter()


@router.get("/emails")
def get_emails(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):

    credentials = Credentials(
        token=user.access_token,
        refresh_token=user.refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET")
    )


    if not credentials.valid:
        try:
            credentials.refresh(Request())
        except Exception as e:
            raise Exception(f"Token refresh failed: {str(e)}")

    service = get_gmail_service(credentials)

    emails = fetch_unread_emails(service)
    for msg in emails:

        detail = get_email_detail(
            service,
            msg["id"]
        )

        parsed = parse_email_data(detail)

        exists = db.query(Email).filter(
            Email.gmail_message_id == msg["id"],
            Email.user_id == user.id
        ).first()

        if not exists:
            email = Email(
                gmail_message_id=msg["id"],
                sender=extract_email(parsed["sender"]),
                subject=parsed["subject"],
                body=parsed["body"],
                user_id=user.id
            )

            db.add(email)

    db.commit()
    return {
        "message": "success",
        "count": len(emails)
    }

@router.post("/send/{draft_id}")
def send_draft(
    draft_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):

    credentials = Credentials(
        token=user.access_token,
        refresh_token=user.refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET")
    )

    service = get_gmail_service(credentials)

    draft = db.query(Draft).filter(
        Draft.id == draft_id,
        Draft.user_id == user.id
    ).first()

    if not draft:
        raise HTTPException(
            status_code=404,
            detail="Draft not found"
        )

    email = db.query(Email).filter(
        Email.id == draft.email_id,
        Email.user_id == user.id
    ).first()

    send_email(
        service,
        email.sender,
        f"Re: {email.subject}",
        draft.generated_reply
    )

    draft.status = "sent"

    db.commit()

    return {
        "message": "Email sent"
    }