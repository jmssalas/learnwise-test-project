import os
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from .database_interface import DatabaseInterface
from .models import Conversation


class SQLite(DatabaseInterface):
    def __init__(self, database_url: str):
        connect_args = (
            {"check_same_thread": False}
            if database_url.startswith("sqlite")
            else {}
        )
        self.engine = create_engine(database_url, connect_args=connect_args)
        self.SessionLocal = sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
        )
        self.__db = self.SessionLocal()

    def create(self, data: dict) -> dict:
        conversation = Conversation(**self.__normalize_data(data))
        self.__db.add(conversation)
        self.__db.commit()
        self.__db.refresh(conversation)
        return self.__serialize(conversation)

    def update(self, data: dict) -> dict:
        conversation_id = data.get("id")
        if not conversation_id:
            raise ValueError("Conversation id is required")

        conversation = self.__db.get(Conversation, conversation_id)
        if conversation is None:
            raise ValueError(f"Conversation not found: {conversation_id}")

        for field, value in self.__normalize_data(data).items():
            if field != "id":
                setattr(conversation, field, value)

        self.__db.commit()
        self.__db.refresh(conversation)
        return self.__serialize(conversation)

    def list(self) -> list[dict]:
        conversations = self.__db.scalars(
            select(Conversation).order_by(Conversation.created_at)
        ).all()
        return [self.__serialize(conversation) for conversation in conversations]

    def close(self) -> None:
        self.__db.close()
        self.engine.dispose()

    @staticmethod
    def __normalize_data(data: dict) -> dict[str, Any]:
        normalized = {
            "id": data.get("id"),
            "phone_number": data.get("phone_number", data.get("phoneNumber")),
            "incoming_message": data.get(
                "incoming_message", data.get("incomingMessage")
            ),
            "llm_response": data.get("llm_response", data.get("llmResponse")),
            "provider_message_id": data.get(
                "provider_message_id", data.get("providerMessageId")
            ),
            "status": data.get("status"),
            "created_at": data.get("created_at", data.get("createdAt")),
        }

        if isinstance(normalized["created_at"], str):
            normalized["created_at"] = datetime.fromisoformat(
                normalized["created_at"].replace("Z", "+00:00")
            )

        return {key: value for key, value in normalized.items() if value is not None}

    @staticmethod
    def __serialize(conversation: Conversation) -> dict:
        created_at = conversation.created_at
        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)

        return {
            "id": conversation.id,
            "phoneNumber": conversation.phone_number,
            "incomingMessage": conversation.incoming_message,
            "llmResponse": conversation.llm_response,
            "providerMessageId": conversation.provider_message_id,
            "status": conversation.status,
            "createdAt": created_at.isoformat(),
        }
