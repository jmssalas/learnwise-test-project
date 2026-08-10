from app.controllers import sms as sms_controller
from app.services.storage.storage_service import StorageService


class FakeLLMService:
    def __init__(self, response: str = "Generated answer") -> None:
        self.response = response
        self.messages: list[str] = []

    def generate_response(self, message: str) -> str:
        self.messages.append(message)
        return self.response


class FakeSMSProvider:
    def __init__(self, sent: bool = True) -> None:
        self.sent = sent
        self.messages: list[tuple[str, str]] = []

    def send_sms(self, message: str, phone_number: str) -> bool:
        self.messages.append((message, phone_number))
        return self.sent


def sms_payload(message_id: str = "SM123") -> dict[str, str]:
    return {
        "phoneNumber": "+36123456789",
        "body": "How do I reset my password?",
        "messageId": message_id,
        "timestamp": "2026-07-27T12:00:00Z",
    }


def test_sms_endpoint_persists_completed_conversation(client, database, monkeypatch) -> None:
    llm = FakeLLMService()
    provider = FakeSMSProvider(sent=True)
    monkeypatch.setattr(sms_controller, "storage", StorageService(database))
    monkeypatch.setattr(sms_controller, "llmService", llm)
    monkeypatch.setattr(sms_controller, "smsProvider", provider)

    response = client.post("/v1/sms/", json=sms_payload())

    assert response.status_code == 200
    assert response.json() is True
    assert llm.messages == ["How do I reset my password?"]
    assert provider.messages == [("Generated answer", "+36123456789")]
    conversation = database.list()[0]
    assert conversation["status"] == "completed"
    assert conversation["llmResponse"] == "Generated answer"


def test_sms_endpoint_marks_failed_delivery_as_error(client, database, monkeypatch) -> None:
    monkeypatch.setattr(sms_controller, "storage", StorageService(database))
    monkeypatch.setattr(sms_controller, "llmService", FakeLLMService())
    monkeypatch.setattr(sms_controller, "smsProvider", FakeSMSProvider(sent=False))

    response = client.post("/v1/sms/", json=sms_payload())

    assert response.status_code == 200
    assert database.list()[0]["status"] == "error"


def test_feedback_endpoint_updates_latest_conversation(client, database, monkeypatch) -> None:
    storage = StorageService(database)
    storage.create_conversation({
        "phoneNumber": "+36123456789",
        "incomingMessage": "Question",
        "llmResponse": "Answer",
        "providerMessageId": "SM123",
        "status": "completed",
        "createdAt": "2026-07-27T12:00:00Z",
    })
    monkeypatch.setattr(sms_controller, "storage", storage)

    response = client.post(
        "/v1/sms/feedback",
        json={"phoneNumber": "+36123456789", "feedback": "👍"},
    )

    assert response.status_code == 200
    assert response.json() is True
    assert database.list()[0]["feedback"] == "positive"


def test_feedback_endpoint_returns_false_without_conversation(client, database, monkeypatch) -> None:
    monkeypatch.setattr(sms_controller, "storage", StorageService(database))

    response = client.post(
        "/v1/sms/feedback",
        json={"phoneNumber": "+36123456789", "feedback": "0"},
    )

    assert response.status_code == 200
    assert response.json() is False


def test_sms_endpoint_rejects_invalid_payload(client) -> None:
    response = client.post("/v1/sms/", json={"body": "missing fields"})

    assert response.status_code == 422
