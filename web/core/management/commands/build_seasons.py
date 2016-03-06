import calendar
from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils.dateparse import parse_date

import nflgame
import pytz

from ...models import Season, Game, Drive, Play, Player


def create_datetime(date_string):
    naive_date = parse_date(date_string)
    timestamp1 = calendar.timegm(naive_date.timetuple())
    datetime1 =  datetime.utcfromtimestamp(timestamp1)
    return pytz.utc.localize(datetime1)


def build_season(season):
    pass


def build_game(game):
    pass


def build_drive(drive):
    pass


def build_play(play):
    pass


class Command(BaseCommand):
    help = 'used to rebuild accounts from csv file'

    def handle(self, *args, **options):

        if not options.get('csv_file_name'):
            raise CommandError("Please pass a csv_file in")

        for season in settings.SEASONS_SUPPORTED:
            pass