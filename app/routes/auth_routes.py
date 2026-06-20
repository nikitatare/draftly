from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from google_auth_oauthlib.flow import Flow
from app.core.dependencies import get_db
from app.models.user import User
from app.core.security import create_access_token
from app.core.dependencies import get_current_user
from googleapiclient.discovery import build


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
    db.refresh(user)

    jwt_token = create_access_token(
        {
            "sub": user.email
        }
    )

    return {
        "success": True,
        "email": gmail_email,
        "access_token": jwt_token,
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

