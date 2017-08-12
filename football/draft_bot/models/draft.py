from datetime import datetime

from django.db import models
from model_utils.models import TimeStampedModel

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
    teams = models.ForeignKey('draft_bot.Team')

    def __str__(self):
        return "{} Season".format(self.season)

    @classmethod
    def new_draft(cls):
        """
        Creates new teams and players for a draft.
        """
        all_players = Players.objects.all()
        if len(all_players) == 0:
            raise ValueError("Did you remember to create players?")

        new_draft = cls.objects.create(season=datetime.now().year,
                                         available_players=all_players)

        for owner in settings.LEAGUE_SETTINGS:
            owner_config = settings.LEAGUE_SETTINGS[owner]
            draft_position = owner_config.draft_position
            new_team = Team.objects.create(owner=owner,
                                           draft=new_draft,
                                           draft_position=draft_position)

            owner_config = settings.LEAGUE_SETTINGS[owner]
            for keeper in owner_config.keepers:
                new_team.add_player(keeper.playerid)

            new_draft.teams.add(new_team)

        return new_draft

    def print_top_available_players(self, position="QB", n=15):
        """
        """

    def make_pick(self, draft_position):

        try:
            current_team = Team.objects.get(draft_position=draft_position)
        except Team.DoesNotExist:
            print("Draft position {} does not have a team!")
            return

        options = {
            "d": "Draft bot suggestion",
            "m": "Make a pick",
            "u": "Unstage pick",
            "c": "Commit staged pick",
            "t": "Change team (current team is wrong)",
            "s": "Show top players",
        }

        staged_pick = None
        final_pick = None
        current_team.print_roster()
        choice = "bligyblag"
        # keep going till pick is made
        while not final_pick:
            while choice not in options:
                for option in options:
                    print("{}  -> {}".format(option, options[option]))

                choice = raw_input("What would you like to do?")
                if option == "m":
                    player = raw_input("Which Player would you like to pick? (either playerid or name)")
                    available_players = self.available_players.all()
                    if type(player) == int:
                        try:
                            staged_pick = self.available_players.get(playerid=player)
                        except Player.DoesNotExist:
                            print("{} doesnt exist! try again".format(player))
                            continue

                    selected_players = available_players.filter(full_name__contains=player)
                    if not selected_players:
                        print("Couldnt find a matching player! Try again")
                        continue

                elif option == "u":

                    if staged_pick:
                        staged_pick = Nonee
                    else:
                        print("No staged pick!")
                        continue

                elif option == "c":
                    final_pick = staged_pick
                    continue

                elif option == "t":
                    self.print_teams()
                    position = raw_input("Which team should be current?")
                    new_team = self.teams.get(draft_position=position)
                    continue

                elif option == "s":
                    position = raw_input("Which position? (leave blank for all\
                                        players)")
                    self.print_top_available_players(position=position, n=15)

                elif option == "d":
                    # TODO: code up draft bot suggestion
                    continue


                else:
                    print("Invalid choice!")
                    continue

        current_team.make_pick(final_pick)

