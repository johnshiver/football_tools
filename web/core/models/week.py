from django.db import models

from model_utils.models import TimeStampedModel


class Week(TimeStampedModel):
    season = models.ForeignKey('core.Season', related_name='weeks')
    number = models.SmallIntegerField()

    def __str__(self):
        return "Week {}".format(self.number)

    def top_scorers(self, limit=10):
        return self.weekly_stats.all().order_by('-total_score')[:limit]

    def top_rushers(self, limit=5):
        """
        """
        if not limit:
            limit = -1
        return self.weekly_stats.all().order_by('rushing_yds')[:limit]

    def top_passer(self, limit=5):
        """
        """
        if not limit:
            limit = -1
        return self.weekly_stats.all().order_by('-passing_yds')[:limit]

    def top_receivers(self, limit=5):
        """
        """
        if not limit:
            limit = -1
        return self.weekly_stats.all().order_by('-receiving_yds')[:limit]
