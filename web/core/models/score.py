from django.db import models

from model_utils import Choices
from model_utils.models import TimeStampedModel

from .player import Player
from .game import Game
from .play import Play
from .drive import Drive


class Score(TimeStampedModel):

    SCORE_TYPE_CHOICES = Choices(
        (0, "PASSING_TD"),
        (1, "RUSHING_TD"),
        (2, "DEFENSIVE_TD"),
        (3, "FIELD_GOAL"),
        (4, "EXTRA_POINT"),
        (5, "SAFETY"),
    )

    points = models.IntegerField()
    scoring_type = models.IntegerField(choices=SCORE_TYPE_CHOICES)

    players = models.ManyToManyField(Player, related_name='scores')
    game = models.ForeignKey(Game, related_name='scores')
    play = models.ForeignKey(Play, related_name='score')
    drive = models.ForeignKey(Drive, related_name='score')
