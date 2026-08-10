from datetime import datetime

from pydantic import BaseModel


class Conversation(BaseModel):
    """API model representing a conversation."""

    id: str
    phoneNumber: str
    incomingMessage: str
    llmResponse: str
    providerMessageId: str
    status: str
    createdAt: datetime
    feedback: str