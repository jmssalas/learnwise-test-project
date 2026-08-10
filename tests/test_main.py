from fastapi.testclient import TestClient

from app.main import app


def test_admin_conversations_placeholder() -> None:
    response = TestClient(app).get("/admin/conversations", params={"phoneNumber": "+36123456789"})

    assert response.status_code == 200
    assert response.json() == [{"status": "@TODO"}]
