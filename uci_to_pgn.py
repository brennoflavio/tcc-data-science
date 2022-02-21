import chess
import sys
import chess.pgn

board = chess.Board()

moves = sys.argv[1:]

for x in moves:
    board.push(chess.Move.from_uci(x))


def export_game(board):
    game = chess.pgn.Game()

    node = game.add_variation(board.move_stack[0])

    for i, x in enumerate(board.move_stack):
        if i > 0:
            node = node.add_variation(x)
    return game


print(export_game(board))
