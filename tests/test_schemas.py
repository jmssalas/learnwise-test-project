from datetime import datetime

import pytest
from pydantic import ValidationError

from app.schemas.conversation import Conversation
from app.schemas.feedback import Feedback
from app.schemas.sms import SMS


def test_sms_accepts_valid_payload() -> None:
    sms = SMS(
        phoneNumber="+36123456789",
        body="Hello",
        messageId="SM123",
        timestamp="2026-07-27T12:00:00Z",
    )

    assert sms.phoneNumber == "+36123456789"


def test_sms_requires_all_fields() -> None:
    with pytest.raises(ValidationError):
        SMS(phoneNumber="+36123456789", body="Hello", messageId="SM123")


def test_feedback_accepts_phone_and_value() -> None:
    feedback = Feedback(phoneNumber="+36123456789", feedback="👍")

    assert feedback.feedback == "👍"


def test_conversation_parses_created_at() -> None:
    conversation = Conversation(
        id="conv_123",
        phoneNumber="+36123456789",
        incomingMessage="Hello",
        llmResponse="Hi",
        providerMessageId="SM123",
        status="completed",
        createdAt="2026-07-27T12:00:00Z",
        feedback="none",
    )

    assert conversation.createdAt == datetime.fromisoformat("2026-07-27T12:00:00+00:00")