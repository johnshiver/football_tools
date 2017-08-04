from django.db import models

from model_utils.models import TimeStampedModel


class Draft(TimeStampedModel):
    season = models.SmallIntegerField()
    available_players = models.ManyToManyField('core.Player')

    def __str__(self):
        return "{} Season".format(self.season)
