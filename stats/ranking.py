from game.models import Game, Player, ScoreTeam, Team
import trueskill
from matplotlib import pyplot
import numpy


def plot_ranking_history(rankings_history):
    fig = pyplot.figure(figsize=(10, 5))
    ax = fig.add_subplot(111)
    player_rankings = {}
    for rankings in rankings_history:
        for player, ranking in rankings.items():
            if player == 'admin':
                continue
            if player not in player_rankings:
                player_rankings[player] = {}
                player_rankings[player]['mu'] = []
                player_rankings[player]['sigma'] = []
            # if len(player_rankings[player]['mu']) > 0 and player_rankings[player]['mu'][-1] == ranking.mu:
            #     continue
            player_rankings[player]['mu'].append(ranking.mu)
            player_rankings[player]['sigma'].append(ranking.sigma)
    for player, y in player_rankings.items():
        t = numpy.arange(len(y['mu']))
        ax.plot(y['mu'], label=player)
        sigma = numpy.array(y['sigma'])
        mu = numpy.array(y['mu'])
        ax.fill_between(t, mu - sigma/5, mu + sigma/5, alpha=0.2)

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels, loc='upper left')
    fig.tight_layout()
    fig.savefig('test.png')


def calculate_trueskill_rating_history():
    games = Game.objects.all()
    # games = list(games)
    # games = games[-int(len(games)/2):]
    players = Player.objects.all()
    env = trueskill.TrueSkill(draw_probability=0.0)
    player_ratings = {}
    rankings_history = []
    for player in players:
        player_ratings[player.name] = env.create_rating()
    for game in games:
        rating_groups = []
        ranks = []
        for team in game.teams.all():
            rating_group = {}
            for player in team.players.all():
                # print(player)
                rating_group[player.name] = player_ratings[player.name]
            if game.team_win.id == team.id:
                ranks.append(0)
            else:
                ranks.append(1)
            rating_groups.append(rating_group)
        # print('{:.1%} chance to draw'.format(env.quality(rating_groups)))
        # print('ranks: ', ranks)
        # print('ranks: ', game.team_scores_list)
        # print('rating groups: ', rating_groups)
        game_ratings = env.rate(rating_groups=rating_groups, ranks=ranks)
        for game_rating in game_ratings:
            for player, rating in game_rating.items():
                # print(rating)
                player_ratings[player] = rating
        print(game)
        current_ranking = {}
        for player, rating in player_ratings.items():
            print(player, rating.mu, rating.sigma)
            current_ranking[player] = rating
        rankings_history.append(current_ranking)
        # print('player ratings: ', player_ratings)
    print('===============\n')
    for player, rating in player_ratings.items():
        print(player, rating.mu, rating.sigma)
    print(rankings_history)
    plot_ranking_history(rankings_history)

