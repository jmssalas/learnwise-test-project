from datetime import datetime
import os

from fastapi import APIRouter
from dotenv import load_dotenv

from app.db.sqlite import SQLite
from app.schemas.sms import SMS
from app.schemas.conversation import Conversation
from app.services.llm.llm_service_factory import LLMServiceFactory
from app.services.sms.sms_provider_factory import SMSProviderFactory
from app.services.storage.storage_service import StorageService

STATUS = {
    "RECEIVED": "received",
    "LLM_RESPONDED": "llmResponded",
    "COMPLETED": "completed",
    "ERROR": "error",
}


router = APIRouter(
    prefix="/v1/sms",
    tags=["sms"]
)

load_dotenv()

database_url = os.getenv("DATABASE_URL")
database = SQLite(database_url)
storage = StorageService(database)

llmType = os.getenv("LLM_SERVICE")
llmService = LLMServiceFactory.create(type=llmType)

smsType = os.getenv("SMS_PROVIDER")
smsProvider = SMSProviderFactory.create(type=smsType)


@router.post("/")
async def sms(sms: SMS) -> bool:
    """Receive incoming SMS messages from the SMS Provider."""

    # @TODO: Handle errors and exceptions, and update the conversation status accordingly

    conversation = storage.create_conversation({
        "phoneNumber": sms.phoneNumber,
        "incomingMessage": sms.body,
        "providerMessageId": sms.messageId,
        "status": STATUS["RECEIVED"],
        "llmResponse": "",
        "createdAt": sms.timestamp or datetime.now().isoformat(),
    })

    response = llmService.generate_response(conversation.incomingMessage)

    conversation = storage.update_conversation(conversation.id, {
        "llmResponse": response,
        "status": STATUS["LLM_RESPONDED"],
    })

    sent = smsProvider.send_sms(response, conversation.phoneNumber)

    conversation = storage.update_conversation(conversation.id, {
        "status": STATUS["COMPLETED"] if sent else STATUS["ERROR"],
    })

    return True


@router.post("/feedback")
async def feedback() -> dict[str, str]:
    """Receive feedback of the most recent conversation."""
    # @TODO: Implement SMS receiving logic here
    return {"status": "@TODO"}
