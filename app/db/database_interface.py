
from abc import ABC, abstractmethod


class DatabaseInterface(ABC):
    @abstractmethod
    def create(self, data: dict) -> dict:
        pass

    @abstractmethod
    def update(self, data: dict) -> dict:
        pass

    @abstractmethod
    def list(self) -> list[dict]:
        pass
