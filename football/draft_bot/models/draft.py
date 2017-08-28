from datetime import datetime

from django.conf import settings
from django.db import models
from model_utils.models import TimeStampedModel

from terminaltables import AsciiTable

from .team import Team
from core.models import Player


class Draft(TimeStampedModel):
    """
    This is the model that connects all the other data models,
    so this is the one to look at first!

    Contains relations to players + teams.
    """
    season = models.SmallIntegerField()
    available_players = models.ManyToManyField('core.Player')
    teams = models.ManyToManyField(Team)

    def __str__(self):
        return "{} Season".format(self.season)

    @classmethod
    def new_draft(cls):
        """
        Creates new teams and players for a draft.
        """
        all_players = Player.objects.all()
        if len(all_players) == 0:
            raise ValueError("Did you remember to create players?")
        new_draft = cls.objects.create(season=datetime.now().year)
        new_draft.available_players.add(*all_players)

        teams = Team.objects.all()
        if not teams:
            teams = []
            for owner in settings.LEAGUE_SETTINGS:
                owner_config = settings.LEAGUE_SETTINGS[owner]
                draft_position = owner_config.draft_position
                new_team = Team.objects.create(owner=owner,
                                               draft_position=draft_position)

                owner_config = settings.LEAGUE_SETTINGS[owner]
                for keeper in owner_config.keepers:
                    k = Player.objects.filter(full_name=keeper)
                    if not k:
                        print("Couldnt find keeper {}".format(keeper))
                        continue
                    elif len(k) > 1:
                        best = 0
                        p = None
                        for k in k:
                            if k.draft_bot_score > best:
                                best = k.draft_bot_score
                                p = k
                        k = p
                    else:
                        k = k[0]

                    new_team.add_player(k.playerid, draft=new_draft)

                teams.append(new_team)

        new_draft.teams.add(*teams)
        return new_draft

    def print_teams(self):
        teams = self.teams.all()
        teams = sorted(teams, key=lambda x: x.draft_position)
        for team in teams:
            print("{} - {}".format(team.draft_position, team))

    def print_top_available_players(self, position='QB', n=15):
        valid_positions = Player.POSITION_CHOICES
        # reduce tuples to single element
        valid_positions = map(lambda x: x[0], valid_positions)
        if position and position not in valid_positions:
            raise ValueError("{} must be one of {}".format(position,
                                                           valid_positions))

        table_data = [
            ['ID', 'Player', 'Position', 'Points'],
        ]

        players = self.available_players.all()
        if position:
            players = players.filter(position=position)
        top_players = sorted(players, key=lambda x: x.draft_bot_score,
                             reverse=True)
        for player in top_players[:n]:
            table_data.append([player.playerid, player.full_name, player.position,
                               int(player.draft_bot_score)])

        table = AsciiTable(table_data)
        print(table.table)

    def make_pick(self, draft_position):
        try:
            current_team = Team.objects.get(draft_position=draft_position)
        except Team.DoesNotExist:
            print("Draft position {} does not have a team!")
            return

        options = {
            #            "d": "Draft bot suggestion",
            "m": "Make a pick",
            "u": "Unstage pick",
            "c": "Commit staged pick",
            "t": "Change team (current team is wrong)",
            "s": "Show top players",
            "p": "Print all rosters",
            "k": "Skip this selection",

        }

        staged_pick = None
        final_pick = None
        # keep going till pick is made
        skip_pick = object()
        while not final_pick:
            choice = "bligyblag"
            while choice not in options:
                print("{} - {}".format(draft_position, current_team))
                print("staged pick: {}".format(staged_pick))
                current_team.print_roster()
                for option in options:
                    print("{}  -> {}".format(option, options[option]))
                choice = raw_input("What would you like to do?")

                #import ipdb;ipdb.set_trace()
                #------------------ option methods ---------------------------#
                if choice == "m":
                    playerid = raw_input("Which Player would you like to pick? (either playerid or name)")
                    try:
                        staged_pick = self.available_players.get(playerid=playerid)
                    except Player.DoesNotExist:
                        print("{} doesnt exist! try again".format(player))
                        continue


                elif choice == "u":
                    if staged_pick:
                        staged_pick = None
                    else:
                        print("No staged pick!")
                        continue

                elif choice == "c":
                    final_pick = staged_pick
                    continue

                elif choice == "t":
                    self.print_teams()
                    position = raw_input("Which team should be current?")
                    current_team = self.teams.get(draft_position=position)
                    continue

                elif choice == "s":
                    position = raw_input(
                        "Which position? (leave blank for all players)")
                    self.print_top_available_players(position=position)

                elif choice == "p":
                    for team in self.teams.all():
                        team.print_roster()
                    continue

#                elif option == "d":
#                    # TODO: code up draft bot suggestion
#                    continue

                elif choice =="k":
                    final_pick = skip_pick

                else:
                    print("Invalid choice!")
                    continue
        if not final_pick == skip_pick:
            current_team.add_player(final_pick.playerid, draft=self)

