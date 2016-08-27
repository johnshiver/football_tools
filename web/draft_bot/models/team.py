from django.db import models

from model_utils.models import TimeStampedModel


class Team(TimeStampedModel):

    owner = models.ForeignKey('draft_bot.Owner')
    draft = models.ForeignKey('draft_bot.Draft')
    # TODO: should roster be a separate model?
    players = models.ManyToManyField('core.Player')

    name = models.CharField(max_length=250)

    def __str__(self):
        return "{}'s {}".format(self.owner,
                                self.name)

    def save(self, force_insert=False,
             force_update=False, using=None,
             update_fields=None):

        # TODO: Validate team roster on save

        super(Team, self).save(force_insert,
                               force_update,
                               using,
                               update_fields)

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

        return final_string
