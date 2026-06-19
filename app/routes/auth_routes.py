from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from google_auth_oauthlib.flow import Flow
from app.core.dependencies import get_db
from app.models.user import User
from app.schemas.auth_schema import RegisterRequest, LoginRequest
from app.services.auth_service import hash_password, verify_password
from app.core.security import create_access_token
from app.core.dependencies import get_current_user
from googleapiclient.discovery import build
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify"
]

CLIENT_SECRETS_FILE = "credentials.json"

flow = Flow.from_client_secrets_file(
    CLIENT_SECRETS_FILE,
    scopes=SCOPES,
    redirect_uri="http://localhost:8001/auth/google/callback"
)

@router.get("/google/login")
def login():

    auth_url, _ = flow.authorization_url(
        access_type="offline",
        prompt="consent"
    )

    return {
        "auth_url": auth_url
    }


@router.get("/google/callback")
def callback(
    code: str,
    db: Session = Depends(get_db)
):

    flow.fetch_token(code=code)

    credentials = flow.credentials
    print("ACCESS TOKEN EXISTS:", credentials.token is not None)
    print("REFRESH TOKEN:", credentials.refresh_token)
    from googleapiclient.discovery import build

    service = build(
        "gmail",
        "v1",
        credentials=credentials
    )

    profile = service.users().getProfile(
        userId="me"
    ).execute()

    gmail_email = profile["emailAddress"]

    user = db.query(User).filter(
        User.email == gmail_email
    ).first()

    if user:
        user.access_token = credentials.token
        user.refresh_token = credentials.refresh_token

    else:
        user = User(
            email=gmail_email,
            access_token=credentials.token,
            refresh_token=credentials.refresh_token
        )

        db.add(user)

    db.commit()

    return {
        "success": True,
        "email": gmail_email
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
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(
            User.email == form_data.username
        )
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not verify_password(
        form_data.password,
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