from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.email import Email
from app.models.draft import Draft

router = APIRouter()


@router.get("/stats")
def get_stats(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):

    total_emails = db.query(Email).filter(
        Email.user_id == user.id
    ).count()

    total_drafts = db.query(Draft).filter(
        Draft.user_id == user.id
    ).count()

    total_sent = db.query(Draft).filter(
        Draft.user_id == user.id,
        Draft.status == "sent"
    ).count()

    return {
        "total_emails": total_emails,
        "total_drafts": total_drafts,
        "total_sent": total_sent
    }