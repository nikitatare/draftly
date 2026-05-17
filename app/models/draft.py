from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class Draft(Base):
    __tablename__ = "drafts"

    id = Column(Integer, primary_key=True)
    email_id = Column(Integer)
    generated_reply = Column(Text)
    status = Column(String)

