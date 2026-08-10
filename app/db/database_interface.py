
from abc import ABC, abstractmethod
from app.db.models import Conversation

class DatabaseInterface(ABC):
    @abstractmethod
    def create(self, data: Conversation) -> Conversation:
        pass

    @abstractmethod
    def update(self, id: str, data: Conversation) -> Conversation:
        pass

    @abstractmethod
    def list(self) -> list[Conversation]:
        pass

    @abstractmethod
    def getLastByPhoneNumber(self, phone_number: str) -> Conversation | None:
        pass