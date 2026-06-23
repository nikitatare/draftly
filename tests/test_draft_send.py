from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_send_draft_requires_auth():

    response = client.post("/gmail/send/1")

    assert response.status_code in [401, 403]