from django.core.management.base import BaseCommand

from ...models import WeeklyStats, Player


class Command(BaseCommand):
    def handle(self, *args, **options):
        weekly_stats = WeeklyStats.objects.all()
        for stat in weekly_stats:
            stat.total_score = stat.calc_total_score()
            stat.save()
            print stat
        for player in Player.objects.all():
            player.calculate_draft_bot_score()
