import json
import uuid

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction

from game.models import Game, Team, ScoreTeam, Player


class Command(BaseCommand):
    help = 'Import scores from a custom format'
    players_filepath = 'data/players.json'
    games_filepath = 'data/games.json'

    @transaction.atomic
    def handle(self, *args, **options):
        print('BEGIN: import games')
        Command.create_admin()
        Command.create_users()
        games = Command.create_games()
        for game in games:
            print(game)
        print('END: import games')

    @staticmethod
    def create_admin():
        User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='admin'
        )

    @staticmethod
    def create_users():
        with open(Command.players_filepath, 'r') as players_file:
            players_json = json.load(players_file)
        for username in players_json['players']:
            User.objects.create_user(
                username=username,
                email=username + '@test.com',
                password=uuid.uuid4().hex[:10]
            )

    @staticmethod
    def create_games():
        games = []
        with open(Command.games_filepath, 'r') as players_file:
            games_json = json.load(players_file)
        for game_data in games_json['games']:
            games.append(Command.create_game(game_data))
        return games

    @staticmethod
    def create_game(game_data):
        game = Game.objects.create(max_score=game_data['max_score'])
        for score in game_data['scores']:
            team_players_ids = []
            for name in score['players']:
                team_players_ids.append(Player.get_by_name(name).id)
            team = Team.get_or_create_team(team_players_ids)
            game.teams.add(team)
            ScoreTeam.objects.create(team=team, game=game, score=score['score'])
        game.save()
        return game
