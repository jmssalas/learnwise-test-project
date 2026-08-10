
from app.db.database_interface import DatabaseInterface
from app.schemas.conversation import Conversation


class StorageService:
    def __init__(self, database: DatabaseInterface) -> None:
        self.db = database

    def create_conversation(self, data: Conversation) -> Conversation:
        return Conversation.model_validate(self.db.create(data))

    def update_conversation(self, id: str, data: Conversation) -> Conversation:
        return Conversation.model_validate(self.db.update(id, data))

    def list_conversations(self) -> list[Conversation]:
        return [Conversation.model_validate(item) for item in self.db.list()]

    def update_last_conversation_feedback(self, phone_number: str, feedback: str) -> Conversation | None:
        last_conversation = self.db.getLastByPhoneNumber(phone_number)
        if last_conversation is not None:
            return self.update_conversation(last_conversation.get("id"), {
                "feedback": self.__from_srt_to_feedback(feedback),
            })
        else:
            return None

    def __from_srt_to_feedback(self, feedback_str: str) -> str:
        """Convert feedback string to a valid feedback value."""
        normalized_feedback = feedback_str.strip().lower()

        if normalized_feedback in {"👍", "1"}:
            return "positive"
        if normalized_feedback in {"👎", "0"}:
            return "negative"

        # @TODO: Handle invalid feedback values, e.g., raise an exception or log a warning
        return "none"
