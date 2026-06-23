from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_generate_requires_auth():

    response = client.post("/draft/generate/1")

    assert response.status_code in [401, 403]