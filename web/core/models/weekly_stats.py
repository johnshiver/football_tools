from django.db import models

from model_utils.models import TimeStampedModel


class WeeklyStats(TimeStampedModel):
    player = models.ForeignKey('core.Player', related_name='player_stats')
    season = models.ForeignKey('core.Season')
    week = models.ForeignKey('core.Week', related_name='weekly_stats')

    # rb stats
    rushing_atts = models.SmallIntegerField(default=0)
    rushing_yds = models.IntegerField(default=0)
    rushing_tds = models.IntegerField(default=0)

    # qb stats
    passing_atts = models.SmallIntegerField(default=0)
    passing_cmps = models.IntegerField(default=0)
    passing_yds = models.IntegerField(default=0)
    passing_tds = models.IntegerField(default=0)
    passing_ints = models.SmallIntegerField(default=0)

    # wr stats
    receiving_rec = models.SmallIntegerField(default=0)
    receiving_yds = models.IntegerField(default=0)
    receiving_tds = models.IntegerField(default=0)

    def __str__(self):
        return "{} for {}".format(self.week, self.player)

