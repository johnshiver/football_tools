from django.db import models

from model_utils.models import TimeStampedModel


class Owner(TimeStampedModel):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
