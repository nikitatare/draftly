from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from google_auth_oauthlib.flow import Flow
from app.core.dependencies import get_db
from app.models.user import User
from app.schemas.auth_schema import RegisterRequest, LoginRequest
from app.services.auth_service import hash_password, verify_password
from app.core.security import create_access_token
from app.core.dependencies import get_current_user

router = APIRouter()

SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify"
]

CLIENT_SECRETS_FILE = "credentials.json"

flow = Flow.from_client_secrets_file(
    CLIENT_SECRETS_FILE,
    scopes=SCOPES,
    redirect_uri="http://localhost:8001/auth/callback"
)

@router.get("/login")
def login():

    auth_url, _ = flow.authorization_url(
        access_type="offline",
        prompt="consent"
    )

    return {
        "auth_url": auth_url
    }


@router.get("/callback")
def callback(code: str, db: Session = Depends(get_db)):

    flow.fetch_token(code=code)

    credentials = flow.credentials
    user = User(
        email="nikitatare319@gmail.com",
        access_token=credentials.token,
        refresh_token=credentials.refresh_token
    )

    db.add(user)
    db.commit()


    return {
        "success": True,
        "token_exists": credentials.token is not None
    }

@router.post("/register")
def register(
    payload: RegisterRequest,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == payload.email
    ).first()

    if existing_user:
        return {
            "message": "User already exists"
        }

    user = User(
        email=payload.email,
        hashed_password=hash_password(
            payload.password
        )
    )

    db.add(user)
    db.commit()

    return {
        "message": "User created"
    }

@router.post("/login")
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(
            User.email == request.email
        )
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not verify_password(
        request.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = create_access_token(
        {
            "sub": user.email
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.get("/me")
def me(
    current_user = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "email": current_user.email
    }