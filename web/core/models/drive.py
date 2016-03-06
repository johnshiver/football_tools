from django.db import models

from model_utils.models import TimeStampedModel

from .game import Game
from .team import Team


class Drive(TimeStampedModel):
    game = models.ForeignKey(Game, related_name='drives')
    offense = models.ForeignKey(Team, related_name='offensive_drives')
    defense = models.ForeignKey(Team, related_name='defensive_drives')

    # was it the first / second / third / etc drive
    drive_in_game = models.IntegerField(default=0)
