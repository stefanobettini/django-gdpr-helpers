from .models import LegalReasonGroup, PrivacyLog


class GDPRFormMixin(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        group = LegalReasonGroup.objects.get(where=self.Meta.where)
        for reason in group.get_as_form_fields():
            self.fields[reason["field_name"]] = reason["field"]

    def save(self, *args, **kwargs):
        saved_object = super().save(*args, **kwargs)
        PrivacyLog.objects.create_log(
            content_object=saved_object, cleaned_data=self.cleaned_data
        )
        return saved_object
