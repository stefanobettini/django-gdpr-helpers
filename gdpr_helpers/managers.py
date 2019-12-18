from django import forms
from django.apps import apps
from django.db import models


class LegalReasonManager(models.Manager):
    def get_legal_reasons(self):
        """Return a queryset of active Legal Reasons"""
        return self.filter(active=True)

    def get_as_form_fields(self):
        """Return a list of dict of Legal Reasons fields (booleanField)"""
        fields = []
        for reason in self.get_legal_reasons():
            fields.append(
                {
                    "field_name": reason.field_name,
                    "field": forms.BooleanField(
                        label=reason.flag_text, required=reason.required
                    ),
                }
            )
        return fields


class PrivacyLogManager(models.Manager):
    def _lazy_load_models(self):
        """Lazy load the models so we don't get circular imports problems"""
        self.legal_reason = apps.get_model("privacy", "LegalReason")
        self.privacy_log = apps.get_model("privacy", "PrivacyLog")
        self.privacy_event = apps.get_model("privacy", "PrivacyEvent")

    def create_log(self, user, cleaned_data):
        self._lazy_load_models()
        """Create a new Log using data from a form"""
        privacy_log = self.privacy_log(user=user)
        privacy_log.save()
        for reason in self.legal_reason.objects.get_legal_reasons():
            if reason.field_name in cleaned_data:
                self.privacy_event.objects.create(
                    privacy_log=privacy_log,
                    legal_reason=self.legal_reason.objects.get(
                        pk=reason.field_name.split("privacy_")[1]
                    ),
                    accepted=cleaned_data[reason.field_name],
                )
        return privacy_log
