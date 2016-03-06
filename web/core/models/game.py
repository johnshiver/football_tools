from django.db import models

from model_utils.models import TimeStampedModel

from .team import Team


class Game(TimeStampedModel):
    WEEK_CHOICES = range(1, 17)

    date_played = models.DateTimeField()
    week = models.IntegerField(choices=WEEK_CHOICES)
    home_team = models.ForeignKey(Team, related_name='home_games')
    away_team = models.ForeignKey(Team, related_name='away_games')

    def __repr__(self):
        return "Home: {} vs. Away: {}".format(self.home_team, self.away_team)

    @property
    def winner(self):
        pass

    @property
    def loser(self):
        pass
