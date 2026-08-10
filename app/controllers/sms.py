from datetime import datetime
import os

from fastapi import APIRouter
from dotenv import load_dotenv

from app.db.sqlite import SQLite
from app.schemas.sms import SMS
from app.schemas.conversation import Conversation
from app.services.llm.llm_service_factory import LLMServiceFactory
from app.services.storage.storage_service import StorageService

router = APIRouter(
    prefix="/v1/sms",
    tags=["sms"]
)

load_dotenv()

database_url = os.getenv("DATABASE_URL")
database = SQLite(database_url)
storage = StorageService(database)

type = os.getenv("LLM_SERVICE")
llmService = LLMServiceFactory.create(type=type)


@router.post("/")
async def sms(sms: SMS) -> Conversation:
    """Receive incoming SMS messages from the SMS Provider."""

    # @TODO: Handle errors and exceptions

    conversation = storage.createConversation({
        "phoneNumber": sms.phoneNumber,
        "incomingMessage": sms.body,
        "providerMessageId": sms.messageId,
        "status": "pending",
        "llmResponse": "",
        "createdAt": sms.timestamp or datetime.now().isoformat(),
    })

    response = llmService.generate_response(conversation.incomingMessage)

    conversation = storage.updateConversation(conversation.id, {
        "llmResponse": response,
        "status": "llmResponsed",
    })

    return conversation


@router.post("/feedback")
async def feedback() -> dict[str, str]:
    """Receive feedback of the most recent conversation."""
    # @TODO: Implement SMS receiving logic here
    return {"status": "@TODO"}
