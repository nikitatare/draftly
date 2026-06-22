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
from app.services.google_auth_service import get_valid_credentials
from app.core.dependencies import get_current_user
from app.models.draft import Draft
from app.services.gmail_service import send_email, get_gmail_service, extract_email
from app.utils.logger import logger
from sqlalchemy import or_

router = APIRouter()


@router.get("/emails")
def get_emails(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    credentials = get_valid_credentials(
        user,
        db
    )


    service = get_gmail_service(credentials)

    emails = fetch_unread_emails(service)
    logger.info(
        f"{len(emails)} unread emails fetched for {user.email}"
    )
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
    logger.info(
        f"Emails saved successfully for {user.email}"
    )
    return {
        "message": "success",
        "count": len(emails)
    }

@router.get("/list")
def list_emails(
    page: int = 1,
    limit: int = 20,
    search: str = "",
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    query = db.query(Email).filter(
        Email.user_id == user.id
    )

    # Step 3
    if search:
        query = query.filter(
            or_(
                Email.sender.ilike(f"%{search}%"),
                Email.subject.ilike(f"%{search}%")
            )
        )

    # Step 4
    total_records = query.count()

    emails = (
        query
        .order_by(Email.id.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return {
        "page": page,
        "limit": limit,
        "total_records": total_records,
        "data": [
            {
                "id": email.id,
                "sender": email.sender,
                "subject": email.subject
            }
            for email in emails
        ]
    }

@router.post("/send/{draft_id}")
def send_draft(
    draft_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    credentials = get_valid_credentials(
        user,
        db
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
    logger.info(
        f"Sending email for draft_id={draft.id}"
    )
    draft.status = "sent"

    db.commit()
    logger.info(
        f"Email sent successfully by {user.email}"
    )
    return {
        "message": "Email sent"
    }