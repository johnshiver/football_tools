from django.db import models

from model_utils.models import TimeStampedModel


class Season(TimeStampedModel):
    year = models.IntegerField()

    def __str__(self):
        return "{} Season".format(self.year)

    @staticmethod
    def top_players(stat='rushing_yds', week=None):
        # TODO: fix this shit
        # if week not provided, return for entire season
        if not week:
            weeks = xrange(1, 17)


