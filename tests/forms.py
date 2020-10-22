from django import forms

from gdpr_helpers.forms import GDPRFormMixin
from tests.models import DummyModel


class DummyForm(GDPRFormMixin, forms.ModelForm):
    class Meta:
        model = DummyModel
        where = "registration"
        fields = ("char",)
