from django.db import models

from model_utils.models import TimeStampedModel


class Player(TimeStampedModel):

    POSITION_CHOICES = (
        ("RB", "RB"),
        ("WR", "WR"),
        ("QB", "QB",),
        ("TE", "TE",),
        ("K", "K",)
    )

    team = models.ForeignKey('core.Team', related_name='players')
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=50)
    position = models.CharField(max_length=10, choices=POSITION_CHOICES)
    profile_url = models.CharField(max_length=250)
    # used by nflgame
    playerid = models.CharField(max_length=200)

    # ranking
    avg_adp = models.DecimalField(max_digits=30,
                                  decimal_places=15,
                                  null=True)
    std_dev = models.DecimalField(max_digits=30,
                                  decimal_places=15,
                                  null=True)

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name
