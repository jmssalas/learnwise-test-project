
from .sms_provider_interface import SMSProviderInterface


class MockSMSProvider(SMSProviderInterface):
    def send_sms(self, message: str, phone_number: str) -> bool:
        return True
