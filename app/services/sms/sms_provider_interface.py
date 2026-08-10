from abc import ABC, abstractmethod


class SMSProviderInterface(ABC):
    @abstractmethod
    def send_sms(self, message: str) -> str:
        pass
