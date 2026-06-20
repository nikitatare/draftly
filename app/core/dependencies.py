from app.database import SessionLocal
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

from app.database import SessionLocal
from app.models.user import User
from app.core.security import (
    SECRET_KEY,
    ALGORITHM
)


security = HTTPBearer()

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()





def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    print("TOKEN RECEIVED =", token[:30])

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



    except JWTError as e:

        print("JWT ERROR =", str(e))

        raise HTTPException(

            status_code=401,

            detail=str(e)

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