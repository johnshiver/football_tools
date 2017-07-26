from django.db import models

from model_utils.models import TimeStampedModel


class League(TimeStampedModel):
    name = models.CharField(max_length=200)