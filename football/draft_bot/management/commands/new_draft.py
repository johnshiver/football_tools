import sys

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

import nflgame

from ...models import Draft, Team
from core.models import Player


class Command(BaseCommand):
    help = 'given leage settings defined settings.py create rosters'

    def handle(self, *args, **options):
        draft = Draft.new_draft()

        # create draft order
        up_order = range(1, draft.teams.count()+1)
        down_order = up_order[::-1]

        rounds = settings.ROUNDS
        draft_order = []
        # might fail on odd numbers
        while rounds > 0:
            draft_order.extend(up_order)
            draft_order.extend(down_order)
            rounds -= 2

        rounds = rounds[::-1]
        while rounds:
            draft.make_pick(draft_position=rounds.pop())

