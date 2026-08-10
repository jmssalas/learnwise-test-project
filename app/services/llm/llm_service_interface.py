from abc import ABC, abstractmethod


class LLMServiceInterface(ABC):
    @abstractmethod
    def generate_response(self, message: str) -> str:
        pass
