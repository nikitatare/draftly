from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from app.database import Base
from sqlalchemy.sql import func

class Email(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    gmail_message_id = Column(String,unique=True)
    sender = Column(String)
    subject = Column(String)
    body = Column(Text)
    category = Column(String)
    priority = Column(String)

    created_at = Column(
        DateTime,
        default=func.now()
    )