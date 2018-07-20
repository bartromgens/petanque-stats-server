from django.test import TestCase
from django.contrib.auth.models import User

from game.models import Game, Team, ScoreTeam, Player
from stats.ranking import TrueSkillPlayerRatings


class TestTrueSkill(TestCase):
    password = '12345'

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        for i in range(4):
            User.objects.create_user(username='player ' + str(i), email='player' + str(i) + '@test.com', password=cls.password)
        players = Player.objects.all()
        players_team_a = [players[0], players[1]]
        players_team_b = [players[2], players[3]]
        team_a = Team.create(players_team_a)
        team_b = Team.create(players_team_b)
        print(team_a)
        print(team_b)

        team_a = Team.get_or_create_team([player.id for player in team_a.players.all()])
        team_b = Team.get_or_create_team([player.id for player in team_b.players.all()])
        teams = [team_a, team_b]
        max_score = 13
        score_a = 13
        score_b = 7
        game = Game.create(max_score=max_score, teams=teams)
        ScoreTeam.objects.create(team=team_a, game=game, score=score_a)
        ScoreTeam.objects.create(team=team_b, game=game, score=score_b)
        max_score = 13
        score_a = 7
        score_b = 13
        game = Game.create(max_score=max_score, teams=teams)
        ScoreTeam.objects.create(team=team_a, game=game, score=score_a)
        ScoreTeam.objects.create(team=team_b, game=game, score=score_b)

    def test_true_skill_basic(self):
        players = Player.objects.all()
        games = Game.objects.all()
        ratings = TrueSkillPlayerRatings(players=players, games=games)
        ratings.calculate_rating_history()
        print(ratings)
