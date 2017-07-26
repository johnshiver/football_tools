import sys

from django.core.management.base import BaseCommand, CommandError

import nflgame

from ...models import Player, Team, Season, Week, WeeklyStats


def build_teams():
    for team in nflgame.teams:
        abrv, city, name = team[0], team[1], team[2]
        Team.objects.get_or_create(abrv=abrv,
                                   city=city,
                                   name=name)


def build_players():
    errors = 0
    for player in nflgame.players:
        p = nflgame.players[player]
        try:
            team = Team.objects.get(abrv=p.team)
        except Team.DoesNotExist:
            errors += 1
            continue
        else:
            p, _ = Player.objects.get_or_create(first_name=p.first_name,
                                                last_name=p.last_name,
                                                team=team,
                                                position=p.position,
                                                profile_url=p.profile_url,
                                                playerid=p.playerid
            )
            print(p)

    print errors
    print Player.objects.all().count()


def build_weekly_stats(season=2015, week=1):
    errors = 0
    new_week, _ = Week.objects.get_or_create(season=season,
                                             number=week)
    print "..filling in data for {}".format(new_week)
    games = nflgame.games(season.year, week=week)
    players = nflgame.combine_game_stats(games)

    # qb stats
    for p in players.passing().sort('passing_yds').limit(30):
        try:
            db_player = Player.objects.get(playerid=p.playerid)
        except Player.DoesNotExist:
            errors += 1
            continue
        else:
            weekly_stat, _ = WeeklyStats.objects.get_or_create(player=db_player,
                                                               season=season,
                                                               week=new_week)
            # qb stats
            weekly_stat.passing_attempts = p.passing_attempts
            weekly_stat.passing_cmps = p.passing_cmp
            weekly_stat.passing_yds = p.passing_yds
            weekly_stat.passing_tds = p.passing_tds
            weekly_stat.passing_ints = p.passing_ints
            weekly_stat.save()
    # rushing stats
    for p in players.rushing().sort('rushing_yds').limit(100):
        try:
            db_player = Player.objects.get(playerid=p.playerid)
        except Player.DoesNotExist:
            errors += 1
            continue
        else:
            weekly_stat, _ = WeeklyStats.objects.get_or_create(player=db_player,
                                                               season=season,
                                                               week=new_week)
            weekly_stat.rushing_yds = p.rushing_yds
            weekly_stat.rushing_atts = p.rushing_att
            weekly_stat.rushing_tds = p.rushing_tds
            weekly_stat.save()

    for p in players.receiving().sort('receiving_yds').limit(200):
        try:
            db_player = Player.objects.get(playerid=p.playerid)
        except Player.DoesNotExist:
            errors += 1
            continue
        else:
            weekly_stat, _ = WeeklyStats.objects.get_or_create(player=db_player,
                                                               season=season,
                                                               week=new_week)
            # rec stats
            weekly_stat.receiving_rec = p.receiving_rec
            weekly_stat.receiving_yds = p.receiving_yrds
            weekly_stat.receiving_tds = p.receiving_tds
            weekly_stat.save()


class Command(BaseCommand):
    help = 'used to rebuild accounts from csv file'

    def handle(self, *args, **options):

        build_teams()
        build_players()
        season, _ = Season.objects.get_or_create(year=2016)
        for i in xrange(1, 17):
            build_weekly_stats(season=season, week=i)

