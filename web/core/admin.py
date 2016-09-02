from django.contrib import admin

from models import Player, WeeklyStats


class StatInline(admin.TabularInline):
    model = WeeklyStats

    exclude = ('id', 'created', 'modified')

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields
                if f.name not in self.exclude]


class PlayerAdmin(admin.ModelAdmin):
    """
    """
    ordering = ('avg_adp', )
    list_display = ('full_name', 'position', 'team',
                    'avg_adp', 'std_dev', 'last_season_points')
    list_filter = ('position',)
    search_fields = ('last_name', )

    inlines = [
        StatInline,
    ]

    def last_season_points(self, obj):
        total_points = 0
        for stat in obj.player_stats.all():
            total_points += stat.total_score
        return total_points


class WeeklyStatAdmin(admin.ModelAdmin):
    """
    """
    list_filter = ('player',)

admin.site.register(Player, PlayerAdmin)
admin.site.register(WeeklyStats, WeeklyStatAdmin)
