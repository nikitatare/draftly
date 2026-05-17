from fastapi import APIRouter
from google_auth_oauthlib.flow import Flow

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
def callback(code: str):

    flow.fetch_token(code=code)

    credentials = flow.credentials

    return {
        "success": True,
        "token_exists": credentials.token is not None
    }