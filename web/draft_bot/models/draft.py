# TODO: need some way to keep track of available players
# seems to make sense to do it

from django.db import models

from model_utils.models import TimeStampedModel


class Draft(TimeStampedModel):
    season = models.ForeignKey('core.Season')
    league = models.ForeignKey('draft_bot.League')

    available_players = models.ManyToManyField('core.Players')

    def __str__(self):
        return "{} -> {}".format(self.season, self.league)
