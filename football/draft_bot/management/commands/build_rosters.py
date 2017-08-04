import sys

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

import nflgame

from ...models import Roster, Draft, Team
from core.models import Player


class Command(BaseCommand):
    help = 'given leage settings defined settings.py create rosters'

    def handle(self, *args, **options):

        # create draft
        from datetime import datetime
        all_players = Players.objects.all()
        new_draft = Draft.objects.create(season=datetime.now().year,
                                         available_players=all_players)

        for owner in settings.LEAGUE_SETTINGS:
            new_team = Team.objects.create(owner=owner,
                                           draft=new_draft)

            owner_config = settings.LEAGUE_SETTINGS[owner]
            for keeper in owner_config.keepers:
                new_team.add_player(keeper.playerid)

