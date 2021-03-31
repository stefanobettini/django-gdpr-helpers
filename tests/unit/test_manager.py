import pytest
from django.utils import timezone

from freezegun import freeze_time
from gdpr_helpers.models import PrivacyLog


def test_get_privacy_logs_for_object(registration_legal_reason_group, registration, db):
    log_created = PrivacyLog.objects.create_log(
        content_object=registration,
        cleaned_data={"privacy_registration": True, "privacy_marketing": True}
    )
    log = PrivacyLog.objects.get_privacy_logs_for_object(registration)
    assert log_created == log


@freeze_time("2021-01-01")
def test_get_consents_for_object(registration_legal_reason_group, registration, db):
    expected = [
        {
            "slug": "registration",
            "accepted": True,
            "given_at": timezone.now()
        },
        {
            "slug": "marketing",
            "accepted": False,
            "given_at": timezone.now()
        },
    ]
    log_created = PrivacyLog.objects.create_log(
        content_object=registration,
        cleaned_data={"privacy_registration": True, "privacy_marketing": False}
    )
    assert PrivacyLog.objects.get_consents_for_object(registration) == expected
