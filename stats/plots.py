from matplotlib import pyplot
import numpy
import trueskill

def plot_rating_history(rankings_history, show_range=True, begin=0):
    fig = pyplot.figure(figsize=(10, 6))
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
            player_rankings[player]['mu'].append(ranking.mu - trueskill.MU)
            player_rankings[player]['sigma'].append(ranking.sigma)
    for player, y in player_rankings.items():
        # if len(y['mu']) < 10:
        #     continue
        mu = numpy.array(y['mu'])[begin:]
        sigma = numpy.array(y['sigma'])[begin:]
        t = numpy.arange(len(mu))
        ax.plot(mu, label=player, lw=2)
        if show_range:
            ax.fill_between(t, mu - sigma/6, mu + sigma/6, alpha=0.15)

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels, loc='upper left')
    fig.tight_layout()
    fig.savefig('test.png')
