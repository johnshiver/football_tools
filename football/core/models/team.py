from django.db import models

from model_utils.models import TimeStampedModel


class Team(TimeStampedModel):
    abrv = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    name = models.CharField(max_length=200)

    def __str__(self):
        return "{} {}".format(self.city, self.name)

    def top_rushers(season, week=None):
        """
        """

    def top_passers(season, week=None):
        """
        """

    def top_receivers(season, week=None):
        """
        """

