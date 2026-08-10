from app.schemas.conversation import Conversation


def test_create_returns_api_model(storage) -> None:
    conversation = storage.create_conversation({
        "phoneNumber": "+36123456789",
        "incomingMessage": "Hello",
        "providerMessageId": "SM123",
        "status": "received",
        "llmResponse": "",
        "createdAt": "2026-07-27T12:00:00Z",
    })

    assert isinstance(conversation, Conversation)
    assert conversation.phoneNumber == "+36123456789"


def test_update_last_feedback_uses_latest_conversation(storage) -> None:
    storage.create_conversation({
        "phoneNumber": "+36123456789",
        "incomingMessage": "Hello",
        "providerMessageId": "SM123",
        "status": "completed",
        "llmResponse": "Hi",
        "createdAt": "2026-07-27T12:00:00Z",
    })

    updated = storage.update_last_conversation_feedback("+36123456789", "👍")

    assert updated is not None
    assert updated.feedback == "positive"


def test_update_last_feedback_returns_none_without_conversation(storage) -> None:
    assert storage.update_last_conversation_feedback("+36123456789", "1") is None