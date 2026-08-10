from pydantic import BaseModel


class SMS(BaseModel):
    """Model representing an SMS message."""
    phone_number: str
    body: str
    messageId: str
    timestamp: str | None
