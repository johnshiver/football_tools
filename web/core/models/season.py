from django.conf import settings
from django.db import models

from model_utils.models import TimeStampedModel


class Season(TimeStampedModel):
    year = models.IntegerField(choices=settings.SEASONS_SUPPORTED)

