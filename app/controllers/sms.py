from fastapi import APIRouter

from app.services.llm.llm_service_factory import LLMServiceFactory
from app.services.llm.mock_llm_service import MockLLMService

router = APIRouter(
    prefix="/v1/sms",
    tags=["sms"]
)


@router.post("/")
async def sms() -> dict[str, str]:
    """Receive incoming SMS messages from the SMS Provider."""

    type = "mock" # @TODO: Read this from .env file
    llmService = LLMServiceFactory.create(type=type)
    response = llmService.generate_response()

    return {"status": "ok", "response": response}


@router.post("/feedback")
async def feedback() -> dict[str, str]:
    """Receive feedback of the most recent conversation."""
    # @TODO: Implement SMS receiving logic here
    return {"status": "@TODO"}