from django.db import models

from model_utils.models import TimeStampedModel


class Roster(TimeStampedModel):
    draft = models.ForeignKey('draft_bot.Draft')
    team = models.ForeignKey('draft_bot.Team')
    players = models.ManyToManyField('core.Player')
