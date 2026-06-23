from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
def test_gmail_list_requires_auth():

    response = client.get("/gmail/list")

    assert response.status_code in [401, 403]