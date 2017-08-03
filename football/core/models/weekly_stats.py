from django.db import models
from django.conf import settings

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

    total_score = models.IntegerField(default=0)

    def __str__(self):
        return "{} for {}: score -> {}".format(self.week,
                                               self.player,
                                               self.total_score)

    def calc_total_score(self):
        total = 0
        total += (settings.RUSHING_TD_POINTS * self.rushing_tds)
        total += (settings.RUSHING_YD_POINTS * self.rushing_yds)
        total += (settings.PASSING_YD_POINTS * self.passing_yds)
        total += (settings.PASSING_TD_POINTS * self.passing_tds)
        total += (settings.PASSING_INT_POINTS * self.passing_ints)
        total += (settings.RECEIVING_YD_POINTS * self.receiving_yds)
        total += (settings.RECEIVING_TD_POINTS * self.receiving_tds)
        total += (settings.RECEIVING_REC_POINTS * self.receiving_rec)

        return total
