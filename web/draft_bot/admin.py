from django.contrib import admin

from .models import Team, Draft, League, Roster, Owner


class TeamAdmin(admin.ModelAdmin):
    """
    """


class DraftAdmin(admin.ModelAdmin):
    """
    """


class LeagueAdmin(admin.ModelAdmin):
    """
    """


class RosterAdmin(admin.ModelAdmin):
    """
    """


class OwnerAdmin(admin.ModelAdmin):
    """
    """

admin.site.register(Team, TeamAdmin)
admin.site.register(Draft, DraftAdmin)
admin.site.register(League, LeagueAdmin)
admin.site.register(Roster, RosterAdmin)
admin.site.register(Owner, OwnerAdmin)

