import csv
import json

n_players = 7
players = []
games = []

with open('jdb.csv') as csvfile:
    read_csv = csv.reader(csvfile, delimiter=',')
    read_csv = zip(*read_csv)
    is_first = True
    for row in read_csv:
        if is_first:
            for i in range(n_players):
                players.append(row[3 + i])
            is_first = False
            continue
        game = {
            'location': row[0],
            'date': row[1],
            'max_score': row[2],
            'scores': []
        }
        team_win = []
        team_lose = []
        score_lose = 0
        for i in range(n_players):
            player_score = row[3 + i]
            if player_score != '':
                if player_score == game['max_score']:
                    team_win.append(players[i])
                else:
                    team_lose.append(players[i])
                    score_lose = player_score
        game['scores'] = [
            {
                'players': team_win,
                'score': game['max_score']
            },
            {
                'players': team_lose,
                'score': score_lose
            }
        ]
        games.append(game)

print(games)
print(players)

with open('games.json', 'w') as fp:
    json.dump({'games': games}, fp, indent=2)

with open('players.json', 'w') as fp:
    json.dump({'players': players}, fp, indent=2)
