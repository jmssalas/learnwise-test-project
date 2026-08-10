from .llm_service_interface import LLMServiceInterface
from .mock_llm_service import MockLLMService


class LLMServiceFactory:
    @staticmethod
    def create(type: str = "mock", **kwargs: object) -> LLMServiceInterface:
        if type == "mock":
            return MockLLMService(**kwargs)

        raise ValueError(f"Unsupported LLM service type: {type}")