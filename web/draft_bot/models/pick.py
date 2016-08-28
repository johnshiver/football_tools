from django.db import models

from model_utils.models import TimeStampedModel


class Pick(TimeStampedModel):
    draft = models.ForeignKey('draft_bot.Draft')
    round = models.ForeignKey('draft_bot.Round')
    team = models.ForeignKey('draft_bot.Team')
    player = models.ForeignKey('core.Player')
    number = models.IntegerField(default=0)

