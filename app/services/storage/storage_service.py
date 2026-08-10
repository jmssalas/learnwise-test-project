
from app.db.database_interface import DatabaseInterface
from app.schemas.conversation import Conversation


class StorageService:
    def __init__(self, database: DatabaseInterface) -> None:
        self.db = database

    def createConversation(self, data: Conversation) -> Conversation:
        return Conversation.model_validate(self.db.create(data))

    def updateConversation(self, id: str, data: Conversation) -> Conversation:
        return Conversation.model_validate(self.db.update(id, data))

    def listConversations(self) -> list[Conversation]:
        return [Conversation.model_validate(item) for item in self.db.list()]
