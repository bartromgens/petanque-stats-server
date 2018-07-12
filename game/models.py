from django.db import models
from django.contrib.auth.models import User


class Player(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.username


class Team(models.Model):
    name = models.CharField(max_length=100, null=True, default="", blank=True)
    players = models.ManyToManyField(Player)

    def __str__(self):
        return ' - '.join([player.user.username for player in self.players.all()])

    @staticmethod
    def create(players):
        team = Team.objects.create()
        team.players.set(players)
        team.save()
        return team

    @staticmethod
    def get_or_create_team(player_ids):
        teams = Team.objects.filter(players__in=player_ids)
        for player_id in player_ids:
            teams = teams.filter(players=player_id)
        if teams.exists():
            return teams[0]
        players = Player.objects.filter(id__in=player_ids)
        return Team.create(players)


class Game(models.Model):
    max_score = models.IntegerField(default=13, null=False, blank=False)
    teams = models.ManyToManyField(Team)

    def __str__(self):
        gameStr = '====GAME====\n'
        gameStr += 'max score: ' + str(self.max_score) + '\n'
        for score in self.team_scores:
            gameStr += str(score) + '\n'
        return gameStr

    @property
    def players(self):
        players = []
        for team in self.teams.all():
            players += team.players.all()
        return players

    @property
    def teams_list(self):
        teams_list = []
        for team in self.teams.all():
            teams_list.append(team)
        return teams_list

    @property
    def team_scores(self):
        return ScoreTeam.objects.filter(game=self)

    @property
    def team_scores_list(self):
        if self.team_scores:
            return list(self.team_scores)
        return []

    @property
    def team_win(self):
        for score in self.team_scores:
            if score.score == self.max_score:
                return score.team
        return None

    @property
    def teams_lose(self):
        if self.team_win is not None:
            return self.teams.exclude(id=self.team_win.id)
        return self.teams.all()

    @property
    def teams_lose_list(self):
        return list(self.teams_lose)


class ScoreTeam(models.Model):
    team = models.ForeignKey(Team, null=False, blank=False, on_delete=models.PROTECT)
    game = models.ForeignKey(Game, null=False, blank=False, on_delete=models.CASCADE)
    score = models.IntegerField(default=0, null=False, blank=True)

    def __str__(self):
        return str(self.team) + ' : ' + str(self.score)
