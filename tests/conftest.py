import pytest

from gdpr_helpers.models import LegalReason, LegalReasonGroup, PrivacyLog

from .models import DummyModel


@pytest.fixture
def registration_legal_reason_group(db) -> LegalReasonGroup:
    group = LegalReasonGroup.objects.create(where="registration")
    LegalReason.objects.create(
        legal_group=group,
        required=True,
        active=True,
        flag_text="Required for registration",
    )
    LegalReason.objects.create(
        legal_group=group,
        required=False,
        active=True,
        flag_text="Optional for registration",
    )
    LegalReason.objects.create(
        legal_group=group,
        required=False,
        flag_text="Required for registration, but not active",
    )
    return group


@pytest.fixture
def registration(db) -> DummyModel:
    return DummyModel.objects.create(char="Megatron")


@pytest.fixture
def log(db, registration_legal_reason_group, registration) -> PrivacyLog:
    cleaned_data = {"privacy_1": True, "privacy_2": False}
    return PrivacyLog.objects.create_log(
        content_object=registration, cleaned_data=cleaned_data
    )
