from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Draft(Base):
    __tablename__ = "drafts"

    id = Column(Integer, primary_key=True)

    email_id = Column(
        Integer,
        ForeignKey("emails.id")
    )

    generated_reply = Column(Text)
    edited_reply = Column(Text)

    status = Column(String)

    created_at = Column(
        DateTime,
        default=func.now()
    )