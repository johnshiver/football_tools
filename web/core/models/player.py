from django.db import models

from model_utils.models import TimeStampedModel

from .team import Team


class Player(TimeStampedModel):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=50)

    team = models.ForeignKey(Team, related_name='players')

    def __repr__(self):
        return self.full_name

    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name
