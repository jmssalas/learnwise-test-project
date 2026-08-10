from .sms_provider_interface import SMSProviderInterface
from .mock_sms_service import MockSMSProvider


class SMSProviderFactory:
    @staticmethod
    def create(type: str = "mock", **kwargs: object) -> SMSProviderInterface:
        if type == "mock":
            return MockSMSProvider(**kwargs)

        raise ValueError(f"Unsupported SMS service type: {type}")