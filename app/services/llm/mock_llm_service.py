from .llm_service_interface import LLMServiceInterface


class MockLLMService(LLMServiceInterface):
    def __init__(self, response: str = "Mock response") -> None:
        self.response = response

    def generate_response(self, message: str) -> str:
        return self.response
