import csv

from django.core.management.base import BaseCommand

from ...models import Player


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open("fantasy_stat.csv") as stat_file:
            fantasy_stats = csv.reader(stat_file)
            name = 1
            team = 3
            avg_adp_ = 7
            std_dev_ = 8
            i = 0
            for stat in fantasy_stats:
                i += 1
                if i > 5:
                    first_name, last_name = tuple(stat[name].split())[:2]
                    avg_adp = float(stat[avg_adp_])
                    std_dev = float(stat[std_dev_])
                    team_abrv = stat[team]
                    try:
                        player = Player.objects.filter(first_name=first_name,
                                                       last_name=last_name)
                        if len(player) > 1:
                            player = player.filter(team__abrv=team_abrv)
                        elif len(player) < 1:
                            print "{} {} not found".format(first_name,
                                                           last_name)
                            continue
                    except Exception as e:
                        print "There was an error {}  fetching {} {}".format(e,
                                                                             first_name,
                                                                             last_name)
                    else:
                        player = player.get()
                        player.avg_adp = avg_adp
                        player.std_dev = std_dev
                        print player, player.avg_adp
                        player.save()
