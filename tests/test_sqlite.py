from datetime import datetime, timezone

import pytest
from sqlalchemy.exc import IntegrityError

from app.db.sqlite import SQLite


def conversation_data(**overrides: str) -> dict[str, str]:
    data = {
        "id": "conv_123",
        "phoneNumber": "+36123456789",
        "incomingMessage": "How do I reset my password?",
        "llmResponse": "Use Forgot password.",
        "providerMessageId": "SM123456789",
        "status": "completed",
        "createdAt": "2026-07-27T12:00:00Z",
    }
    data.update(overrides)
    return data


def test_create_serializes_conversation(database: SQLite) -> None:
    result = database.create(conversation_data())

    assert result["id"] == "conv_123"
    assert result["phoneNumber"] == "+36123456789"
    assert result["createdAt"] == "2026-07-27T12:00:00+00:00"


def test_create_generates_id_when_missing(database: SQLite) -> None:
    result = database.create(conversation_data(id=None))

    assert result["id"]


def test_update_changes_only_supplied_fields(database: SQLite) -> None:
    database.create(conversation_data())

    result = database.update("conv_123", {"status": "error"})

    assert result["status"] == "error"
    assert result["incomingMessage"] == "How do I reset my password?"


def test_update_unknown_id_raises_value_error(database: SQLite) -> None:
    with pytest.raises(ValueError, match="Conversation not found"):
        database.update("missing", {"status": "error"})


def test_list_orders_by_created_at(database: SQLite) -> None:
    database.create(conversation_data(
        id="older",
        providerMessageId="SM1",
        createdAt="2026-07-27T11:00:00Z",
    ))
    database.create(conversation_data(
        id="newer",
        providerMessageId="SM2",
        createdAt="2026-07-27T12:00:00Z",
    ))

    assert [item["id"] for item in database.list()] == ["older", "newer"]


def test_get_last_by_phone_number(database: SQLite) -> None:
    database.create(conversation_data(
        id="older",
        providerMessageId="SM1",
        createdAt="2026-07-27T11:00:00Z",
    ))
    database.create(conversation_data(
        id="newer",
        providerMessageId="SM2",
        createdAt="2026-07-27T12:00:00Z",
    ))

    assert database.getLastByPhoneNumber("+36123456789")["id"] == "newer"
    assert database.getLastByPhoneNumber("+34999999999") is None


def test_duplicate_provider_message_rolls_back(database: SQLite) -> None:
    database.create(conversation_data())

    with pytest.raises(IntegrityError):
        database.create(conversation_data(id="second"))

    result = database.create(conversation_data(id="third", providerMessageId="SM3"))
    assert result["id"] == "third"