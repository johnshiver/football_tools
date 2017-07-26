from django.db import models

from model_utils.models import TimeStampedModel


class Round(TimeStampedModel):
    draft = models.ForeignKey('draft_bot.Draft')
    number = models.IntegerField(default=0)

    def make_pick(self, player, team):
        """
        """
