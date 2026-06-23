
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_me_requires_auth():

    response = client.get("/auth/me")

    assert response.status_code in [401, 403]