from app.database import SessionLocal

from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from app.database import SessionLocal
from app.models.user import User
from app.services.auth_service import (
    SECRET_KEY,
    ALGORITHM
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def get_current_user(
    token: str = Depends(oauth2_scheme)
):

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")

        if email is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    db = SessionLocal()

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user