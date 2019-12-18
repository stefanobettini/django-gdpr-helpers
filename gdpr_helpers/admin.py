from django.contrib import admin

from .models import LegalReason, PrivacyEvent, PrivacyLog


class PrivacyEventInline(admin.StackedInline):
    extra = 0
    model = PrivacyEvent


class PrivacyLogAdmin(admin.ModelAdmin):
    fields = ("user", "created")
    readonly_fields = ("created",)
    inlines = [PrivacyEventInline]


admin.site.register(LegalReason)
admin.site.register(PrivacyEvent)
admin.site.register(PrivacyLog, PrivacyLogAdmin)
