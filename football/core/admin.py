from django.contrib import admin

from models import Player


class PlayerAdmin(admin.ModelAdmin):
    """
    """

admin.site.register(Player, PlayerAdmin)
