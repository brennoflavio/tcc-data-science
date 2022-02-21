import chess.pgn
import random
from uuid import uuid4

number_of_games = 16639  # 99% confidence, 1% error
total_games = 93679328
games_list = []

for _ in range(number_of_games):
    games_list.append(random.randint(0, total_games))

with open("data") as pgn:
    i = 0
    for _ in range(total_games):
        game = chess.pgn.read_game(pgn)
        if i in games_list:
            print(i)
            with open(f"./games/{uuid4()}.pgn", "w+") as f:
                f.write(str(game))
                f.write("\n\n")
                f.flush()
        i += 1
