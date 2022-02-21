import chess
import chess.engine
import sqlite3
import pickle
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path


def is_accurate(board, engine, next_move):
    try:
        info = engine.analyse(board, chess.engine.Limit(time=5), multipv=5)
    except Exception:
        return None, None

    best_moves = [x["pv"][0] for x in info]

    if next_move in best_moves:
        return True, info
    else:
        return False, info


def parse_game(moves, engine, id=None, return_data=False, print_data=True):
    if print_data:
        print(f"doing game {id}")

    board = chess.Board()

    total_moves = 0
    accurate_moves = 0
    engine_response = []

    for i, x in enumerate(moves.split(" ")):
        if print_data:
            print(f"Doing move {str(i)}")

        try:
            next_move = chess.Move.from_uci(moves.split(" ")[i + 1])
        except Exception:
            break

        board.push(chess.Move.from_uci(x))

        total_moves += 1
        accurate, engine_info = is_accurate(board, engine, next_move)

        if accurate and accurate is not None:
            accurate_moves += 1

        engine_response.append(engine_info)

    if return_data:
        return {
            "total_moves": total_moves,
            "accurate_moves": accurate_moves,
            "engine_info": engine_response,
        }
    else:
        with open(f"./engine_data/{str(id)}.pickle", "wb+") as p_file:
            p_file.write(
                pickle.dumps(
                    {
                        "total_moves": total_moves,
                        "accurate_moves": accurate_moves,
                        "engine_info": engine_response,
                    }
                )
            )
            p_file.flush()


def main(x):
    engine = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish")

    parse_game(x[1], engine, x[0])

    engine.quit()


if __name__ == "__main__":
    conn = sqlite3.connect("games.db")
    cursor = conn.cursor()

    games = cursor.execute("select id, moves from games")
    games = games.fetchall()

    fs = list(Path("./engine_data").rglob("*"))

    fs = [str(x).replace("engine_data/", "").replace(".pickle", "") for x in fs]

    games = [x for x in games if int(x[0]) not in [int(y) for y in fs]]

    with ProcessPoolExecutor(20) as pool:
        futures = []
        for x in games:
            futures.append(pool.submit(main, x))

        for x in futures:
            x.result()
