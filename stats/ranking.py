from game.models import Game, Player, ScoreTeam, Team
import trueskill
from stats import plots


def plot_rating_history():
    players = Player.objects.exclude(user__username='admin')
    games = Game.objects.all()
    rating = TrueSkillPlayerRatings(players, games)
    rating.calculate_rating_history()
    rating.plot_history()
    print(rating)


class TrueSkillPlayerRatings(object):

    def __init__(self, players, games):
        self.players = players
        self.games = games
        self.env = trueskill.TrueSkill(draw_probability=0.0)
        self.player_ratings = self.create_initial_ratings(self.players)
        self.ratings_history = []

    def __str__(self):
        ratings_str = 'RATINGS:\n'
        for player, rating in self.player_ratings.items():
            ratings_str += '{}: {:.1f} ({:.2f})'.format(player, rating.mu, rating.sigma)
            ratings_str += '\n'
        return ratings_str

    def create_initial_ratings(self, players):
        player_ratings = {}
        for player in players:
            player_ratings[player.name] = self.env.create_rating()
        return player_ratings

    def calculate_rating_history(self):
        self.ratings_history = []
        for game in self.games:
            current_rating = self.update_rating_for_game(game)
            self.ratings_history.append(current_rating)
        return self.ratings_history, self.player_ratings

    def update_rating_for_game(self, game):
        rating_groups = []
        ranks = []
        for team in game.teams.all():
            rating_group = {}
            for player in team.players.all():
                rating_group[player.name] = self.player_ratings[player.name]
            if game.team_win.id == team.id:
                ranks.append(0)
            else:
                ranks.append(1)
            rating_groups.append(rating_group)
        game_ratings = self.env.rate(rating_groups=rating_groups, ranks=ranks)
        for game_rating in game_ratings:
            for player, rating in game_rating.items():
                self.player_ratings[player] = rating
        current_ratings = {}
        for player, rating in self.player_ratings.items():
            current_ratings[player] = rating
        return current_ratings

    def plot_history(self):
        plots.plot_rating_history(self.ratings_history, begin=20)


# def calculate_trueskill_team_rating_history():
#     games = Game.objects.all()
#     teams = Team.objects.all()
#     env = trueskill.TrueSkill(draw_probability=0.0)
#     team_rankings = {}
#     rankings_history = []
#     for team in teams:
#         team_rankings[str(team)] = env.create_rating()
#     for game in games:
#         rating_groups = []
#         ranks = []
#         for team in game.teams.all():
#             rating_group = {
#                 str(team): team_rankings[str(team)]
#             }
#             if game.team_win.id == team.id:
#                 ranks.append(0)
#             else:
#                 ranks.append(1)
#             rating_groups.append(rating_group)
#         game_ratings = env.rate(rating_groups=rating_groups, ranks=ranks)
#         for game_rating in game_ratings:
#             for player, rating in game_rating.items():
#                 team_rankings[player] = rating
#         print(game)
#         current_ranking = {}
#         for player, rating in team_rankings.items():
#             print(player, rating.mu, rating.sigma)
#             current_ranking[player] = rating
#         rankings_history.append(current_ranking)
#     print('===============\n')
#     for player, rating in team_rankings.items():
#         print(player, rating.mu, rating.sigma)
#     print(rankings_history)
#     plots.plot_ranking_history(rankings_history, show_range=False)


# def calculate_team_win_probability():
#     rankings_history, player_ratings = calculate_trueskill_rating_history()
#     print(player_ratings)
#     teams = Team.objects.all()
#     team1 = teams[0]
#     team_rankings1 = []
#     for player in team1.players.all():
#         team_rankings1.append(player_ratings[player.name])
#     team2 = teams[1]
#     team_rankings2 = []
#     for player in team2.players.all():
#         team_rankings2.append(player_ratings[player.name])
#     win_prob = win_probability(team_rankings1, team_rankings2)
#     print(team1, team2, win_prob)
#
#
# def win_probability(team1, team2):
#     delta_mu = sum(r.mu for r in team1) - sum(r.mu for r in team2)
#     sum_sigma = sum(r.sigma ** 2 for r in itertools.chain(team1, team2))
#     size = len(team1) + len(team2)
#     denom = math.sqrt(size * (trueskill.BETA * trueskill.BETA) + sum_sigma)
#     ts = trueskill.global_env()
#     return ts.cdf(delta_mu / denom)
