from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import LegalReasonManager, PrivacyLogManager


class PrivacyLog(models.Model):
    """A new log will be created when a user accept some flags"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name=_("Utente"),
        related_name="privacy",
    )
    created = models.DateTimeField(_("Data creazione"), auto_now_add=True)

    objects = PrivacyLogManager()

    def __str__(self):
        return f"{self.user} privacy-log {self.created}"

    class Meta:
        verbose_name = _("Privacy log")
        verbose_name_plural = _("Privacy logs")


class LegalReason(models.Model):
    """Register the legal reason, it will be used for flags and privacy-policy page"""

    flag_text = models.TextField(_("Testo da mostrare nella spunta"))
    privacy_description = models.TextField(
        _("Descrizione per pagina privacy"), blank=True, null=True
    )
    required = models.BooleanField(_("Obbligatorio"), default=False)
    active = models.BooleanField(_("Attivo"), default=False)

    objects = LegalReasonManager()

    @property
    def field_name(self):
        return f"privacy_{self.pk}"

    def __str__(self):
        return self.flag_text

    class Meta:
        verbose_name = _("Ragione legale")
        verbose_name_plural = _("Ragioni legali")


class PrivacyEvent(models.Model):
    """Register user consent"""

    privacy_log = models.ForeignKey(
        PrivacyLog,
        on_delete=models.PROTECT,
        verbose_name=_("Privacy log"),
        related_name="event",
    )
    legal_reason = models.ForeignKey(
        LegalReason,
        on_delete=models.PROTECT,
        verbose_name=_("Ragione legale"),
        related_name="event",
    )
    accepted = models.BooleanField(_("Accetata"), default=False)

    def __str__(self):
        return f"{self.legal_reason} {self.accepted}"

    class Meta:
        verbose_name = _("Evento privacy")
        verbose_name_plural = _("Eventi privacy")
