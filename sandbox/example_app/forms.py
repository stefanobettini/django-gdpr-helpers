from django import forms
from gdpr_helpers.forms import GDPRFormMixin

from .models import ExampleModel


class ExampleForm(GDPRFormMixin, forms.ModelForm):
    class Meta:
        model = ExampleModel
        where = "contact_form"
        exclude = ()
