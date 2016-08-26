from django.db import models

from model_utils.models import TimeStampedModel


class Season(TimeStampedModel):
    year = models.IntegerField()

    def __str__(self):
        return "{} Season".format(self.year)

