from django.contrib import admin

from models import Player


class PlayerAdmin(admin.ModelAdmin):
    """

    """
    ordering = ('avg_adp', )
    list_display = ('full_name', 'team', 'avg_adp', 'std_dev')

admin.site.register(Player, PlayerAdmin)
