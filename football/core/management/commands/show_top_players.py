import sys

from django.core.management.base import BaseCommand, CommandError

import nflgame
from terminaltables import AsciiTable

from ...models import Player, Team, Season, Week, WeeklyStats


class Command(BaseCommand):
    help = 'takes option position, displays top players as table'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('position', nargs=1)


    def handle(self, *args, **options):

        p = options['position']
        if p:
            Player.show_top_players(position=p[0])
        else:
            Player.show_top_players()
