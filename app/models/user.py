from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)

    hashed_password = Column(String)

    access_token = Column(String)
    refresh_token = Column(String)
    created_at = Column(
        DateTime,
        default=func.now()
    )
