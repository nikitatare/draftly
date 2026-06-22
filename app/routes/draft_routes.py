from fastapi import APIRouter, Depends, HTTPException
from openai import OpenAI
import os
from dotenv import load_dotenv

from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.models.email import Email
from app.models.draft import Draft

from app.services.google_auth_service import get_valid_credentials
from app.core.dependencies import get_current_user

from app.services.ai_service import generate_reply
from app.utils.logger import logger

from app.models.user import User

from app.services.gmail_service import get_gmail_service

load_dotenv(override=True)

router = APIRouter()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


@router.post("/generate/{email_id}")
def generate(
    email_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    email = db.query(Email).filter(
        Email.id == email_id,
        Email.user_id == user.id
    ).first()

    if not email:
        logger.warning(
            f"Email not found: {email_id}"
        )
        raise HTTPException(
            status_code=404,
            detail="Email not found"
        )
    logger.info(
        f"Generating draft for email_id={email.id}"
    )
    ai_reply = generate_reply(email.body, tone="friendly")
    # Get logged-in user

    # Create credentials
    credentials = get_valid_credentials(
        user,
        db
    )

    # Gmail service
    service = get_gmail_service(credentials)

    # Mark email as read in Gmail
    service.users().messages().modify(
        userId="me",
        id=email.gmail_message_id,
        body={
            "removeLabelIds": ["UNREAD"]
        }
    ).execute()

    draft = Draft(
        email_id=email.id,
        user_id=user.id,
        generated_reply=ai_reply,
        status="drafted"
    )

    db.add(draft)
    db.commit()
    logger.info(
        f"Draft generated successfully for email_id={email.id}"
    )
    return {
        "reply": ai_reply
    }