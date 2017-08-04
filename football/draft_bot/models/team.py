from django.db import models

from model_utils.models import TimeStampedModel

from core.models import Player


class Team(TimeStampedModel):

    owner = models.CharField(max_length=250)
    draft = models.ForeignKey('draft_bot.Draft')
    players = models.ManyToManyField('core.Player',
                                     related_name='fantasy_team')

    name = models.CharField(max_length=250)

    def __str__(self):
        return "{}'s {}".format(self.owner,
                                self.name)

    def add_player(self, player_id):
        try:
            player = Player.objects.get(playerid=player_id)
        except Player.DoesNotExist:
            print("{} doesnt exist in db!")
        else:
            if player not in self.draft.available_players.all():
                print("{} has already been selected! try again".format(player))
                return
            self.players.add(player)
            self.draft.available_players.remove(player)

    def show_roster(self):
        qbs = self.players.filter(postion='QB')
        rbs = self.players.filter(postion='RB')
        wrs = self.players.filter(postion='WR')

        final_string = ""
        final_string += "--------QBS--------"
        for qb in qbs:
            final_string += "{}\n".format(qb.full_name)

        final_string = ""
        final_string += "--------RBS--------"
        for rb in rbs:
            final_string += "{}\n".format(rb.full_name)

        final_string = ""
        final_string += "--------WRS--------"
        for wr in wrs:
            final_string += "{}\n".format(wr.full_name)

        print(final_string)
