from rest_framework import serializers, viewsets
from django.contrib.auth.models import User

from game import models


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.User
        fields = ('id', 'url', 'username',)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = models.Player
        fields = ('id', 'url', 'user',)


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = models.Player.objects.all()
    serializer_class = PlayerSerializer


class ScoreTeamSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.ScoreTeam
        fields = ('id', 'url', 'team', 'game', 'score', 'team_id')


class ScoreTeamViewSet(viewsets.ModelViewSet):
    queryset = models.ScoreTeam.objects.all()
    serializer_class = ScoreTeamSerializer


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    players = PlayerSerializer(read_only=True, many=True)

    class Meta:
        model = models.Team
        fields = ('id', 'url', 'players',)


class TeamViewSet(viewsets.ModelViewSet):
    queryset = models.Team.objects.all()
    serializer_class = TeamSerializer


class GameSerializer(serializers.HyperlinkedModelSerializer):
    teams = TeamSerializer(read_only=True, many=True)
    scores = ScoreTeamSerializer(read_only=True, many=True, source='scoreteam_set')

    class Meta:
        model = models.Game
        fields = ('id', 'url', 'teams', 'max_score', 'scores')


class GameViewSet(viewsets.ModelViewSet):
    queryset = models.Game.objects.all()
    serializer_class = GameSerializer

