from django.contrib.auth.models import User

from rest_framework import serializers, viewsets, views
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from game.models import Player, ScoreTeam, Team, Game


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'url', 'username',)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Player
        fields = ('id', 'url', 'user',)


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class ScoreTeamSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ScoreTeam
        fields = ('id', 'url', 'team', 'game', 'score', 'team_id')


class ScoreTeamViewSet(viewsets.ModelViewSet):
    queryset = ScoreTeam.objects.all()
    serializer_class = ScoreTeamSerializer


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    players = PlayerSerializer(read_only=True, many=True)

    class Meta:
        model = Team
        fields = ('id', 'url', 'players',)


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class GameSerializer(serializers.HyperlinkedModelSerializer):
    teams = TeamSerializer(read_only=True, many=True)
    scores = ScoreTeamSerializer(read_only=True, many=True, source='scoreteam_set')

    class Meta:
        model = Game
        fields = ('id', 'url', 'teams', 'max_score', 'scores')


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def create(self, request, *args, **kwargs):
        print(request.data)
        max_score = request.data['maxScore']
        players_team_a = request.data['playersTeamA']
        players_team_b = request.data['playersTeamB']
        score_a = request.data['scoreTeamA']
        score_b = request.data['scoreTeamB']
        players_team_a_ids = GameViewSet.get_team_player_ids(players_team_a)
        players_team_b_ids = GameViewSet.get_team_player_ids(players_team_b)
        team_a = Team.get_or_create_team(players_team_a_ids)
        team_b = Team.get_or_create_team(players_team_b_ids)
        teams = [team_a, team_b]
        game = GameViewSet.create_game(max_score=max_score, teams=teams)
        ScoreTeam.objects.create(team=team_a, game=game, score=score_a)
        ScoreTeam.objects.create(team=team_b, game=game, score=score_b)
        print(game)
        self.kwargs['pk'] = game.id
        return self.retrieve(request)

    @staticmethod
    def get_team_player_ids(team_players):
        team_player_ids = []
        for player in team_players:
            team_player_ids.append(player["id"])
        return team_player_ids

    @staticmethod
    def create_game(max_score, teams):
        game = Game.objects.create(max_score=max_score)
        game.teams.set(teams)
        game.save()
        return game
