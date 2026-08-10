from pydantic import BaseModel


class SMS(BaseModel):
    """Model representing an SMS message."""
    phoneNumber: str
    body: str
    messageId: str
    timestamp: str | None
