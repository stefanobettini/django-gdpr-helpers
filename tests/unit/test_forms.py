import pytest
from django import forms

from gdpr_helpers.models import PrivacyEvent, PrivacyLog
from tests.forms import DummyForm
from tests.models import DummyModel


def test_legal_reason_group_as_form_fields(registration_legal_reason_group):
    form_fields = registration_legal_reason_group.get_as_form_fields()
    assert len(form_fields) == 2
    assert form_fields[0]["field_name"] == "privacy_1"
    assert isinstance(form_fields[0]["field"], forms.BooleanField)
    assert form_fields[1]["field_name"] == "privacy_2"
    assert isinstance(form_fields[1]["field"], forms.TypedChoiceField)


def test_form_has_legal_reason_group_fields(registration_legal_reason_group):
    form = DummyForm()
    assert "privacy_1" in form.fields
    assert "privacy_2" in form.fields
    assert "privacy_3" not in form.fields


@pytest.mark.parametrize("privacy_1, privacy_1_valid", [(True, True), (False, False)])
@pytest.mark.parametrize("privacy_2, privacy_2_valid", [(True, True), (False, True)])
def test_form_is_valid(
    registration_legal_reason_group,
    privacy_1,
    privacy_2,
    privacy_1_valid,
    privacy_2_valid,
):
    form = DummyForm(
        {"char": "Megatron", "privacy_1": privacy_1, "privacy_2": privacy_2}
    )
    assert form.is_valid() == all([privacy_1_valid, privacy_2_valid])


def test_form_works_without_legal_reasons(db):
    form = DummyForm({"char": "Megatron"})
    assert "privacy_1" not in form.fields
    assert "privacy_2" not in form.fields
    assert form.is_valid() is True


def test_form_save_object(db):
    form = DummyForm({"char": "Megatron"})
    obj = form.save()
    assert DummyModel.objects.count() == 1
    assert obj == DummyModel.objects.get(pk=1)


def test_log_is_generated(registration_legal_reason_group, registration, db):
    PrivacyLog.objects.create_log(
        content_object=registration, cleaned_data={"privacy_1": True, "privacy_2": True}
    )
    assert PrivacyLog.objects.count() == 1
    assert PrivacyEvent.objects.count() == 2


def test_log_are_correct(log):
    event_1 = PrivacyEvent.objects.get(privacy_log=log, legal_reason__pk=1)
    event_2 = PrivacyEvent.objects.get(privacy_log=log, legal_reason__pk=2)
    assert event_1.accepted is True
    assert event_2.accepted is False
