from django.db import models

from model_utils.models import TimeStampedModel

from .drive import Drive


class Play(TimeStampedModel):
    drive = models.ForeignKey(Drive, related_name='plays')

