from django.db import models

from model_utils.models import TimeStampedModel

from core.models import Player



class Team(TimeStampedModel):

    owner = models.CharField(max_length=250)
    players = models.ManyToManyField('core.Player',
                                     related_name='fantasy_team')
    draft_position = models.SmallIntegerField()

    def __str__(self):
        return str(self.owner)

    def add_player(self, player_id, draft):
        try:
            player = Player.objects.get(playerid=player_id)
        except Player.DoesNotExist:
            print("{} doesnt exist in db!")
        else:
            if player not in draft.available_players.all():
                print("{} has already been selected! try again".format(player))
                return
            self.players.add(player)
            draft.available_players.remove(player)

    def remove_player(self, player_id):
        try:
            player = Player.objects.get(playerid=player_id)
        except Player.DoesNotExist:
            print("{} doesnt exist in db!")
        else:
            if player not in self.players.all():
                print("{} not on team!".format(player))
                return
            self.players.remove(player)
            self.draft.available_players.add(player)

    def print_roster(self):
        print "#" * 45
        print(str(self) + "'s Team")
        qbs = self.players.filter(position='QB')
        rbs = self.players.filter(position='RB')
        wrs = self.players.filter(position='WR')

        final_string = ""
        final_string += "\n"
        final_string += "--------QBS--------\n"
        for qb in qbs:
            final_string += "{} {}\n".format(qb.full_name,
                                             int(qb.draft_bot_score))

        final_string += "\n"
        final_string += "--------RBS--------\n"
        for rb in rbs:
            final_string += "{} {}\n".format(rb.full_name,
                                             int(rb.draft_bot_score))

        final_string += "\n"
        final_string += "--------WRS--------\n"
        for wr in wrs:
            final_string += "{} {}\n".format(wr.full_name,
                                             int(wr.draft_bot_score))

        print(final_string)
