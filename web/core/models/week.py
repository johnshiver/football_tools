from django.db import models

from model_utils.models import TimeStampedModel


class Week(TimeStampedModel):
    season = models.ForeignKey('core.Season', related_name='weeks')
    number = models.SmallIntegerField()

    def __str__(self):
        return "{}: Week {}".format(self.season, self.number)
