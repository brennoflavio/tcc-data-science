import sqlite3
from pathlib import Path
import chess.pgn
from statistics import mean


def get_moves(game):
    all_moves = ""
    for move in game.mainline_moves():
        all_moves = f"{all_moves} {str(move)}"

    return all_moves.lstrip()


def get_opening(moves):
    opening_database_final = {
        "e2e4 g8f6": "Alekhines Defence",
        "d2d4 g8f6 c2c4 c7c5 d4d5": "Benoni Defense",
        "d2d4 g8f6 c2c4 e7e6 g2g3": "Catalan Opening",
        "e2e4 c7c6": "Caro-Kann Defence",
        "e2e4 e7e6": "French Defence",
        "d2d4 g8f6 c2c4 g7g6 b1c3 d7d5": "Grunfeld-Indian",
        "d2d4 f7f5": "Dutch Defence",
        "e2e4 e7e5 g1f3 b8c6 f1c4": "Italian Game",
        "e2e4 g7g6": "Kings Fianchetto",
        "e2e4 e7e5 f2f4": "Kings Gambit",
        "d2d4 g8f6 c2c4 g7g6 b1c3 f8g7 e2e4 d7d6": "Kings Indian",
        "d2d4 g8f6 c2c4 e7e6 b1c3 Bb4": "Nimzo-Indian",
        "d2d4 g8f6 c2c4 d7d6": "Old Indian",
        "e2e4 d7d6": "Pirc Defence",
        "d2d4 d7d5 c2c4 d5c4": "Queens Gambit Accepted",
        "d2d4 g8f6 c2c4 e7e6 g1f3 b7b6": "Queens Indian",
        "d2d4 d7d5 c2c4 e7e6": "Queens Gambit",
        "e2e4 e7e5 g1f3 g8f6": "Russian Game-Petroff",
        "e2e4 e7e5 g1f3 b8c6 f1b5": "Ruy Lopez-Spanish",
        "e2e4 d7d5": "Scandinavian Defence",
        "e2e4 c7c5": "Sicilian Defence",
        "d2d4 d7d5 c2c4 c7c6": "Slav Defence",
        "d2d4 d7d5 c2c4 c7c6 g1f3 g8f6 b1c3 e7e6": "Semi-Slav Defense",
        "e2e4 e7e5 g1f3 b8c6 d2d4": "Scotch Opening",
        "e2e4 e7e5 b1c3": "Vienna Game",
        "c2c4": "English Opening",
        "e2e4 e7e5 f1c4": "Bishops Opening",
        "e2e4 e7e5": "Kings Pawn Openings",
        "d2d4 g8f6": "Queens Pawn Openings g8f6",
        "d2d4 d7d5": "Queens Pawn Openings d7d5",
        "g1f3": "Reti Opening",
        "d2d4": "Queens Pawn Openings d4",
    }

    for k, v in opening_database_final.items():
        if moves.startswith(k):
            return v

    return "Other Opening"


def get_average_elo(game):
    return mean([int(game.headers["WhiteElo"]), int(game.headers["BlackElo"])])


def calculate_tier(elo):
    return int(elo / 200.00)


if __name__ == "__main__":
    conn = sqlite3.connect("games.db")

    cursor = conn.cursor()

    cursor.execute(
        "create table games (id int, moves text, opening text, elo int, elo_tier text, file_id text, event text)"
    )
    conn.commit()

    i = 0
    for f in Path("./games").rglob("*"):
        i += 1
        with open(f) as pgn:
            game = chess.pgn.read_game(pgn)

            moves = get_moves(game)

            opening = get_opening(moves)

            elo = get_average_elo(game)

            tier = calculate_tier(elo)

            cursor.execute(
                "insert into games (id, moves, opening, elo, elo_tier, file_id, event) values (?, ?, ?, ?, ?, ?, ?)",
                (i, moves, opening, elo, tier, str(f), game.headers["Event"]),
            )

    conn.commit()
