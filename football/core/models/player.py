from datetime import datetime

from django.db import models
import nflgame

from model_utils.models import TimeStampedModel

from .weekly_stats import WeeklyStats


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
    age = models.SmallIntegerField(null=True)
    # used by nflgame
    playerid = models.CharField(max_length=200)

    # TODO: this isnt meant to stick around, since season specific
    total_pts = models.SmallIntegerField(null=True)
    first_half_pts = models.SmallIntegerField(null=True)
    second_half_pts = models.SmallIntegerField(null=True)

    draft_bot_score = models.DecimalField(max_digits=30,
                                          decimal_places=15,
                                          null=True)


    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name

    def calculate_age(self, players=None, recalc=False):
        """
        Optionally pass in players, seems better than importing everytime.
        """
        if not self.age or self.recalc:
            if not players:
                players = nflgame.players

            this_player = players[self.playerid]
            age_dt = datetime.strptime(this_player.birthdate, "%m/%d/%Y")
            age = datetime.now() - age_dt
            self.age = age.days / 360
            # TODO: add update fields arg, will increase save performance
            print("{} is {}".format(self.full_name, self.age))
            self.save()

    def calculate_draft_bot_score(self):
        """
        RE-calculates draft bot score
        """
        # TODO: set year
        weekly_stats = WeeklyStats.objects.filter(player=self) \
                                          .order_by('week__number')
        if not weekly_stats:
            self.total_pts = 0
            self.first_half_pts = 0
            self.second_half_pts = 0
            self.save()
            return

        first_half, second_half = weekly_stats[:8], weekly_stats[8:]
        first_half_pts = sum([stat.total_score for stat in first_half])
        second_half_pts = sum([stat.total_score for stat in second_half])
        total_pts = first_half_pts + second_half_pts
        print("{} scored {} pnts last year".format(self.full_name,
                                                   total_pts))
        print("{} in first_half".format(first_half_pts))
        print("{} in second_half".format(second_half_pts))
        self.total_pts = total_pts
        self.first_half_pts = first_half_pts
        self.second_half_pts = second_half_pts

        # arbitrary starting number
        draft_bot_pts = 100
        if self.total_pts < 25:

            self.draft_bot_score = 0
            self.save()
            return

        draft_bot_pts += self.total_pts
        if self.first_half_pts > self.second_half_pts and \
           abs(self.first_half_pts - self.second_half_pts) > 50:
            draft_bot_pts -= 15

        if self.first_half_pts and self.second_half_pts == 0:
            draft_bot_pts -= 25


        # yikes this is ugly
        # draft point adjustments based on position / age
        if self.position == "RB":

            # MAX_DRAFT_PENALTY: 20

            # young dudes run faster
            if self.age <= 27:
                draft_bot_pts += 20
            # old dudes do not
            elif self.age > 30:
                draft_bot_pts -= 20
            else:
                draft_bot_pts -= 5


        elif self.position == "WR":
            # MAX_DRAFT_PENALTY: 15

            # young wrs not quite as good
            # if they showed no production, give a stronger penalty
            if self.age < 25:
                if self.total_pts < 50:
                    draft_bot_pts -= 10
                else:
                    draft_bot_pts -= 5

            # these seem like prime years
            elif 24 < self.age < 31:
                draft_bot_pts += 15

            # early 30s still pretty decent
            elif 30 < self.age < 34:
                draft_bot_pts += 5

            # old dudes bad
            else:
                draft_bot_pts -= 15


        elif self.position == "QB":
            # MAX_DRAFT_PENALTY: 15
            # TODO: this should likely be higher

            # young qbs, not as consistent?
            # only penalty if they didnt do great prior season
            if self.age < 25 and self.total_pts < 100:
                draft_bot_pts -= 15

            # prime years, get a boost
            elif 24 < self.age < 36:
                draft_bot_pts += 15

            # really old dudes are bad
            else:
                draft_bot_pts -= 15


        elif self.position == "TE":
            if self.age < 25:
                if self.total_pts < 50:
                    draft_bot_pts -= 10
                else:
                    draft_bot_pts -= 5
            elif 24 < self.age < 31:
                draft_bot_pts += 15
            elif 30 < self.age < 34:
                draft_bot_pts += 5
            else:
                draft_bot_pts -= 15

        self.draft_bot_score = draft_bot_pts
        print("draft bot score = {}".format(self.draft_bot_score))
        self.save()
