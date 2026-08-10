
from .sms_provider_interface import SMSProviderInterface


class MockSMSProvider(SMSProviderInterface):
    def send_sms(self, message: str) -> bool:
        return True
