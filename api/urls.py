
from django.conf.urls import url, include
from django.contrib import admin

from game import api

from rest_framework import serializers, viewsets, routers

# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'scores', api.ScoreTeamViewSet)
router.register(r'games', api.GameViewSet)
router.register(r'teams', api.TeamViewSet)
router.register(r'players', api.PlayerViewSet)
router.register(r'users', api.UserViewSet)

urlpatterns = [
    url(r'^v1/', include(router.urls)),
    url(r'^v1/players/trueskill/history/', api.player_true_skills_ratings_history),
    url(r'^admin/', admin.site.urls),
]


# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns += [
#         url(r'^__debug__/', include(debug_toolbar.urls)),
#     ]
