from datetime import datetime

from django.db import models
from model_utils.models import TimeStampedModel

from ...models import Draft, Team
from core.models import Player


class Draft(TimeStampedModel):
    season = models.SmallIntegerField()
    available_players = models.ManyToManyField('core.Player')
    teams = models.ForeignKey('draft_bot.Team')

    def __str__(self):
        return "{} Season".format(self.season)

    @classmethod
    def new_draft(cls):
        all_players = Players.objects.all()
        if len(all_players) == 0:
            raise ValueError("Did you remember to create players?")

        new_draft = Draft.objects.create(season=datetime.now().year,
                                         available_players=all_players)

        for owner in settings.LEAGUE_SETTINGS:
            owner_config = settings.LEAGUE_SETTINGS[owner]
            draft_position = owner_config.draft_position
            new_team = Team.objects.create(owner=owner,
                                           draft=new_draft,
                                           draft_position=draft_position)

            owner_config = settings.LEAGUE_SETTINGS[owner]
            for keeper in owner_config.keepers:
                new_team.add_player(keeper.playerid)

            new_draft.teams.add(new_team)

        return new_draft
