from django.db import models

from model_utils import Choices
from model_utils.models import TimeStampedModel

from .team import Team


class Player(TimeStampedModel):

    POSITION_CHOICES = Choices(
        (),
    )

    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=50)
    team = models.ForeignKey(Team, related_name='players')
    position = models.IntegerField(choices=POSITION_CHOICES)
    profile_url = models.CharField(max_length=250)
    birth_date = models.DateTimeField()
    college = models.CharField(max_length=100)
    height = models.IntegerField()
    weight = models.IntegerField()

    def __repr__(self):
        return self.full_name

    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name
