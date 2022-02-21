import sys
from build_database import get_moves, get_opening, get_average_elo, calculate_tier
import chess.pgn
from accuracy import parse_game
import chess
import chess.engine
import warnings
from engine_data import std_diff_v2, qualitative_v2
from tablebase import get_tablebase_metrics

f = sys.argv[1]

print(f)

with open(f) as pgn:
    game = chess.pgn.read_game(pgn)

    moves = get_moves(game)
    opening = get_opening(moves)
    elo = get_average_elo(game)
    tier = calculate_tier(elo)

    engine = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish")

    engine_response = parse_game(moves, engine, return_data=True, print_data=True)

    engine.quit()

    total_moves = engine_response.get("total_moves")
    accurate_moves = engine_response.get("accurate_moves")

    event = game.headers["Event"]

    if "bullet" in event.lower():
        time_control = "bullet"
    elif "ultrabullet" in event.lower():
        time_control = "ultrabullet"
    elif "blitz" in event.lower():
        time_control = "blitz"
    elif "rapid" in event.lower():
        time_control = "rapid"
    elif "classical" in event.lower():
        time_control = "classical"
    elif "correspondence" in event.lower():
        time_control = "correspondence"
    else:
        warnings.warn("Time Control not found, need set manually")
        time_control = None

    std_response = std_diff_v2(engine_response)

    evaluation_std_dev = std_response.get("std_dev")
    evaluation_average = std_response.get("average")
    evaluation_median = std_response.get("median")

    qualitative_response = qualitative_v2(engine_response)

    inaccuracies = qualitative_response.get("inaccuracies")
    mistakes = qualitative_response.get("mistakes")
    blunders = qualitative_response.get("blunders")
    greats = qualitative_response.get("greats")
    bests = qualitative_response.get("bests")

    tablebase_metrics = get_tablebase_metrics(moves)

    tablebase_blunders = tablebase_metrics.get("tablebase_blunders")
    tablebase_greats = tablebase_metrics.get("tablebase_greats")


print("moves", moves)
print("opening", opening.lower().replace("-", "_").replace(" ", "_"))
print("elo", elo)
print("tier", tier)
print("total_moves", total_moves)
print("accurate_moves", accurate_moves)
print("time_control", time_control)
print("evaluation_std_dev", evaluation_std_dev)
print("evaluation_average", evaluation_average)
print("evaluation_median", evaluation_median)
print("inaccuracies", inaccuracies)
print("mistakes", mistakes)
print("blunders", blunders)
print("greats", greats)
print("bests", bests)
print("tablebase_blunders", tablebase_blunders)
print("tablebase_greats", tablebase_greats)
