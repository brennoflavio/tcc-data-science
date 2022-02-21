import chess
import chess.syzygy
import sqlite3

if __name__ == "__main__":
    conn = sqlite3.connect("games.db")
    cursor = conn.cursor()

    colors = [chess.BLACK, chess.WHITE]
    pieces = [
        chess.PAWN,
        chess.KNIGHT,
        chess.KING,
        chess.BISHOP,
        chess.ROOK,
        chess.QUEEN,
    ]

    with chess.syzygy.open_tablebase("./3-4-5") as tablebase:
        cursor.execute("select id, moves from games")
        results = cursor.fetchall()

        for result in results:
            print(result[0])

            moves = result[1].split(" ")

            board = chess.Board()

            last_score = None

            tablebase_blunders = 0
            tablebase_greats = 0

            if len(moves) == len([x for x in moves if x]):
                for move in moves:
                    board.push(chess.Move.from_uci(move))

                    piece_number = 0

                    for color in colors:
                        for piece in pieces:
                            piece_number = piece_number + len(
                                board.pieces(piece, color)
                            )

                    if piece_number <= 5:
                        score = tablebase.probe_wdl(board)

                        if abs(score) == 1:
                            score = 0

                        if board.turn:  # White to play
                            adjusted_score = score
                        elif not board.turn:
                            adjusted_score = -1 * score

                        if last_score:
                            score_diff = adjusted_score - last_score

                            if score_diff > 0:
                                tablebase_greats += 1
                            elif score_diff < 0:
                                tablebase_blunders += 1

                        last_score = score

            cursor.execute(
                "update games set tablebase_blunders = ?, tablebase_greats = ? where id = ?",
                (tablebase_blunders, tablebase_greats, result[0]),
            )

        conn.commit()


def get_tablebase_metrics(moves):
    colors = [chess.BLACK, chess.WHITE]
    pieces = [
        chess.PAWN,
        chess.KNIGHT,
        chess.KING,
        chess.BISHOP,
        chess.ROOK,
        chess.QUEEN,
    ]

    with chess.syzygy.open_tablebase("./3-4-5") as tablebase:
        moves = moves.split(" ")

        board = chess.Board()

        last_score = None

        tablebase_blunders = 0
        tablebase_greats = 0

        if len(moves) == len([x for x in moves if x]):
            for move in moves:
                board.push(chess.Move.from_uci(move))

                piece_number = 0

                for color in colors:
                    for piece in pieces:
                        piece_number = piece_number + len(board.pieces(piece, color))

                if piece_number <= 5:
                    score = tablebase.probe_wdl(board)

                    if abs(score) == 1:
                        score = 0

                    if board.turn:  # White to play
                        adjusted_score = score
                    elif not board.turn:
                        adjusted_score = -1 * score

                    if last_score:
                        score_diff = adjusted_score - last_score

                        if score_diff > 0:
                            tablebase_greats += 1
                        elif score_diff < 0:
                            tablebase_blunders += 1

                    last_score = score

    return {
        "tablebase_blunders": tablebase_blunders,
        "tablebase_greats": tablebase_greats,
    }
