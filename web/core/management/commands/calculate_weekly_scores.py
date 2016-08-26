from django.core.management.base import BaseCommand

from ...models import WeeklyStats


class Command(BaseCommand):
    def handle(self, *args, **options):
        weekly_stats = WeeklyStats.objects.all()
        for stat in weekly_stats:
            stat.total_score = stat.calc_total_score()
            stat.save()
            print stat
