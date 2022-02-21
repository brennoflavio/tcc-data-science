import pickle
import sqlite3
from pathlib import Path
import json
import statistics


def accurate_moves():
    for f in Path("./engine_data").rglob("*"):
        with open(f, "rb") as opened_pickle:
            data = pickle.loads(opened_pickle.read())

            print(data.get("total_moves"))
            print(data.get("accurate_moves"))
            print(str(f).split("/")[-1].split(".")[0])

            cursor.execute(
                "update games set total_moves = ?, accurate_moves = ? where id = ?",
                (
                    data.get("total_moves"),
                    data.get("accurate_moves"),
                    int(str(f).split("/")[-1].split(".")[0]),
                ),
            )

    conn.commit()


def parse_event():
    cursor.execute("select id, event from games")
    result = cursor.fetchall()

    for r in result:
        if "bullet" in r[1].lower():
            cursor.execute(
                "update games set time_control = ? where id = ?", ("bullet", r[0])
            )
        elif "ultrabullet" in r[1].lower():
            cursor.execute(
                "update games set time_control = ? where id = ?", ("ultrabullet", r[0])
            )
        elif "blitz" in r[1].lower():
            cursor.execute(
                "update games set time_control = ? where id = ?", ("blitz", r[0])
            )
        elif "rapid" in r[1].lower():
            cursor.execute(
                "update games set time_control = ? where id = ?", ("rapid", r[0])
            )
        elif "classical" in r[1].lower():
            cursor.execute(
                "update games set time_control = ? where id = ?", ("classical", r[0])
            )
        elif "correspondence" in r[1].lower():
            cursor.execute(
                "update games set time_control = ? where id = ?",
                ("correspondence", r[0]),
            )

    conn.commit()


def std_diff():
    cursor.execute("select id, event from games")
    result = cursor.fetchall()

    for r in result:
        print(r[0])
        with open(f"./engine_data/{str(r[0])}.pickle", "rb") as opened_pickle:
            data = pickle.loads(opened_pickle.read())

            score_evolution = []

            for move in data.get("engine_info"):
                if move and not move[0].get("score").is_mate():
                    score_evolution.append(
                        move[0].get("score").white().score() / 100.00
                    )

            if len(score_evolution) > 1:
                std_dev = statistics.stdev(score_evolution)
                average = statistics.mean(score_evolution)
                median = statistics.median(score_evolution)
            else:
                std_dev = None
                average = None
                median = None

            cursor.execute(
                "update games set evaluation = ?, evaluation_average = ?, evaluation_std_dev = ?, evaluation_median = ? where id = ?",
                (json.dumps(score_evolution), average, std_dev, median, r[0]),
            )
    conn.commit()


def std_diff_v2(data):
    score_evolution = []

    for move in data.get("engine_info"):
        if move and not move[0].get("score").is_mate():
            score_evolution.append(move[0].get("score").white().score() / 100.00)

    if len(score_evolution) > 1:
        std_dev = statistics.stdev(score_evolution)
        average = statistics.mean(score_evolution)
        median = statistics.median(score_evolution)
    else:
        std_dev = None
        average = None
        median = None

    return {
        "std_dev": std_dev,
        "average": average,
        "median": median,
    }


def qualitative():
    cursor.execute("select id, event from games")
    result = cursor.fetchall()

    for r in result:
        print(r[0])
        with open(f"./engine_data/{str(r[0])}.pickle", "rb") as opened_pickle:
            data = pickle.loads(opened_pickle.read())

            score_evolution = []

            inaccuracies = 0
            mistakes = 0
            blunders = 0
            greats = 0
            bests = 0

            for move in data.get("engine_info"):
                if move and not move[0].get("score").is_mate():
                    score_evolution.append(
                        (
                            move[0].get("score").white().score() / 100.00,
                            move[0].get("score").turn,
                        )
                    )

            last_score = (0.0, True)  # Board starts equal, white to play

            for score in score_evolution:
                score_diff = score[0] - last_score[0]

                if score_diff >= 2:  # best
                    bests += 1
                elif score_diff >= 1:  # great
                    greats += 1
                elif score_diff <= -3:  # blunder
                    blunders += 1
                elif score_diff <= -2:  # mistake
                    mistakes += 1
                elif score_diff <= -1:  # innacuracy
                    inaccuracies += 1

                last_score = score

            cursor.execute(
                "update games set inaccuracies = ?, mistakes = ?, blunders = ?, greats = ?, bests = ? where id = ?",
                (inaccuracies, mistakes, blunders, greats, bests, r[0]),
            )
    conn.commit()


def qualitative_v2(data):
    score_evolution = []

    inaccuracies = 0
    mistakes = 0
    blunders = 0
    greats = 0
    bests = 0

    for move in data.get("engine_info"):
        if move and not move[0].get("score").is_mate():
            score_evolution.append(
                (
                    move[0].get("score").white().score() / 100.00,
                    move[0].get("score").turn,
                )
            )

    last_score = (0.0, True)  # Board starts equal, white to play

    for score in score_evolution:
        score_diff = score[0] - last_score[0]

        if score_diff >= 2:  # best
            bests += 1
        elif score_diff >= 1:  # great
            greats += 1
        elif score_diff <= -3:  # blunder
            blunders += 1
        elif score_diff <= -2:  # mistake
            mistakes += 1
        elif score_diff <= -1:  # innacuracy
            inaccuracies += 1

        last_score = score

    return {
        "inaccuracies": inaccuracies,
        "mistakes": mistakes,
        "blunders": blunders,
        "greats": greats,
        "bests": bests,
    }


if __name__ == "__main__":
    conn = sqlite3.connect("games.db")
    cursor = conn.cursor()
