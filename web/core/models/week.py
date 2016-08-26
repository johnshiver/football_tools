from django.db import models

from model_utils.models import TimeStampedModel


class Week(TimeStampedModel):
    season = models.ForeignKey('core.Season', related_name='weeks')
    number = models.SmallIntegerField()

    def __str__(self):
        return "{}: Week {}".format(self.season, self.number)
    
    def top_rushers(limit=5):
        """
        """
        if not limit:
            limit = -1
        self.weekly_stats.all().order_by('-rushing_yds')[:limit]

    def top_passer(limit=5):
        """
        """
        if not limit:
            limit = -1
        self.weekly_stats.all().order_by('-passing_yds')[:limit]

    def top_receivers(limit=5):
        """
        """
        if not limit:
            limit = -1
        self.weekly_stats.all().order_by('-rushing_yds')[:limit]
