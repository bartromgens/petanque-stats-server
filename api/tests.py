import json
import uuid

from django.contrib.auth.models import User
from django.test import TestCase
# from rest_framework.test import APITestCase
from django.test import Client

from game.models import Game, Team, ScoreTeam, Player


class TestCaseAdminLogin(TestCase):
    """Test case with client and login as admin function."""
    admin_password = '38dsiha49sd'

    @classmethod
    def setUpTestData(cls):
        User.objects.create_superuser(username='admin', email='admin@test.com', password=cls.admin_password)

    def setUp(self):
        self.client = Client()
        self.login()

    def login(self):
        """Login as admin."""
        success = self.client.login(username='admin', password=self.admin_password)
        self.assertTrue(success)
        response = self.client.get('/admin/', follow=True)
        self.assertEqual(response.status_code, 200)
        return response


class TestAdminPages(TestCaseAdminLogin):

    def test_admin_homepage(self):
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)


class TestPlayer(TestCase):

    def test_create_player_on_user_creation(self):
        username = 'testuser'
        user = User.objects.create_user(
            username=username,
            email=username + '@test.com',
            password=uuid.uuid4().hex[:10]
        )
        players = Player.objects.filter(user=user)
        self.assertTrue(players.exists())
        self.assertEqual(1, players.count())


class TestGame(TestCase):
    password = '123456'

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

    def test_get_games(self):
        url = '/v1/games/'
        print('get games', url)
        response = self.client.get(url)
        print(response.status_code)
        print(response.data)

    def test_create_game_model(self):
        url = '/v1/games/'
        data = {
            'maxScore': 13,
            'playersTeamA': [
                {'id': 0},
                {'id': 1},
            ],
            'playersTeamB': [
                {'id': 2},
                {'id': 3},
            ],
            'scoreTeamA': 10,
            'scoreTeamB': 13
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    # def test_create_game(self):
    #     url = '/v1/create_game/'
    #     data = {
    #         'maxScore': 13,
    #         'playersTeamA': [
    #             '1',
    #         ],
    #         'playersTeamB': [
    #             '2',
    #         ],
    #         'scoreTeamA': 10,
    #         'scoreTeamB': 13
    #     }
    #     print('create game', url, data)
    #     response = self.client.put(url, data=json.dumps(data))
    #     # response = self.client.put(url, data=data)
    #     print(response.status_code)
