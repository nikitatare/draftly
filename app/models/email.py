from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class Email(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True)
    gmail_message_id = Column(String)
    sender = Column(String)
    subject = Column(String)
    body = Column(Text)
