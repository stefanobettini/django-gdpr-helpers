from django.db import models


class DummyModel(models.Model):
    char = models.CharField("Name", max_length=255)
