from pydantic import BaseModel


class Feedback(BaseModel):
    """Model representing feedback for a conversation."""
    phoneNumber: str
    feedback: str
