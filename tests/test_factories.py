import pytest

from app.services.llm.llm_service_factory import LLMServiceFactory
from app.services.llm.mock_llm_service import MockLLMService
from app.services.sms.mock_sms_service import MockSMSProvider
from app.services.sms.sms_provider_factory import SMSProviderFactory


def test_llm_factory_creates_configured_mock() -> None:
    service = LLMServiceFactory.create(response="custom response")

    assert isinstance(service, MockLLMService)
    assert service.generate_response("question") == "custom response"


def test_llm_factory_rejects_unknown_type() -> None:
    with pytest.raises(ValueError):
        LLMServiceFactory.create(type="unknown")


def test_sms_factory_creates_mock_provider() -> None:
    provider = SMSProviderFactory.create()

    assert isinstance(provider, MockSMSProvider)
    assert provider.send_sms("message", "+36123456789") is True


def test_sms_factory_rejects_unknown_type() -> None:
    with pytest.raises(ValueError):
        SMSProviderFactory.create(type="unknown")