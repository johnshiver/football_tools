
from django.core.management.base import BaseCommand, CommandError


from ...models import WeeklyStats


class Command(BaseCommand):

    def handle(self, *args, **options):
	weekly_stats = WeeklyStats.objects.all()
	for stat in weekly_stats:
	    total = stat.cal_total_score()
	    stat.total_score = total
            stat.save()
