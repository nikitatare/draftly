from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_emails_requires_auth():

    response = client.get("/gmail/emails")

    assert response.status_code in [401, 403]