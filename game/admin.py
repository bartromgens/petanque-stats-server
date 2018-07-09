from django.contrib import admin

from game import models


class GameAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'max_score',
        'players',
        'teams_list',
        'team_scores_list',
        'team_win',
        'teams_lose_list',
    )


admin.site.register(models.Game, GameAdmin)
admin.site.register(models.Team, admin.ModelAdmin)
admin.site.register(models.ScoreTeam, admin.ModelAdmin)
admin.site.register(models.Player, admin.ModelAdmin)