import chess
import chess.engine
import chess.pgn

pgn = open("games/0a74a896-4a49-4e27-a210-da1beeea9e5d.pgn")

game = chess.pgn.read_game(pgn)
board = game.board()


all_moves = ""

for move in game.mainline_moves():
    all_moves = f"{all_moves} {str(move)}"
    board.push(move)

all_moves = all_moves.lstrip()

opening_database = {
    "1.e4 Nf6": "Alekhines Defence",
    "1.d4 Nf6 2.c4 c5 3.d5": "Benoni Defense",
    "1.d4 Nf6 2.c4 e6 3.g3": "Catalan Opening",
    "1.e4 c6": "Caro-Kann Defence",
    "1.c4": "English Opening",
    "1.e4 e6": "French Defence",
    "1.d4 Nf6 2.c4 g6 3.Nc3 d5": "Grunfeld-Indian",
    "1.d4 f5": "Dutch Defence",
    "1.e4 e5 2.Nf3 Nc6 3.Bc4": "Italian Game",
    "1.e4 e5 2.Bc4": "Bishops Opening",
    "1.e4 g6": "Kings Fianchetto",
    "1.e4 e5 2.f4": "Kings Gambit",
    "1.d4 Nf6 2.c4 g6 3.Nc3 Bg7 4.e4 d6": "Kings Indian",
    "1.e4 e5": "Kings Pawn Openings",
    "1.d4 Nf6 2.c4 e6 3.Nc3 Bb4": "Nimzo-Indian",
    "1.d4 Nf6 2.c4 d6": "Old Indian",
    "1.e4 d6": "Pirc Defence",
    "1.d4 d5 2.c4 dxc4": "Queens Gambit Accepted",
    "1.d4 Nf6 2.c4 e6 3.Nf3 b6": "Queens Indian",
    "1.d4 d5 2.c4 e6": "Queens Gambit",
    "1.d4 Nf6": "Queens Pawn Openings Nf6",
    "1.d4 d5": "Queens Pawn Openings d5",
    "1.d4": "Queens Pawn Openings d4",
    "1.Nf3": "Reti Opening",
    "1.e4 e5 2.Nf3 Nf6": "Russian Game-Petroff",
    "1.e4 e5 2.Nf3 Nc6 3.Bb5": "Ruy Lopez-Spanish",
    "1.e4 d5": "Scandinavian Defence",
    "1.e4 c5": "Sicilian Defence",
    "1.d4 d5 2.c4 c6": "Slav Defence",
    "1.d4 d5 2.c4 c6 3.Nf3 Nf6 4.Nc3 e6": "Semi-Slav Defense",
    "1.e4 e5 2.Nf3 Nc6 3.d4": "Scotch Opening",
    "1.e4 e5 2.Nc3": "Vienna Game",
}

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
    if k in all_moves:
        print(v)
        break
    print("Other Opening")
