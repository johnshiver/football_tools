from django.contrib import admin

from .models import Team


class TeamAdmin(admin.ModelAdmin):
    """
    """

admin.site.register(Team, TeamAdmin)
