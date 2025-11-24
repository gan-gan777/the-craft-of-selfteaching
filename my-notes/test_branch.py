#!/usr/bin/env python3
# Small terminal game: Number Wizard (guessing game with difficulty, hints, and high scores)

import random
import json
import os
import time

HS_FILE = os.path.join(os.path.expanduser("~"), ".number_wizard_highscores.json")


def load_highscores():
    try:
        with open(HS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"best_score": None, "plays": 0}


def save_highscores(data):
    try:
        with open(HS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except Exception:
        pass


def choose_difficulty():
    print("\nChoose difficulty:")
    print("  1) Easy   (1-20, 7 attempts)")
    print("  2) Normal (1-100, 8 attempts)")
    print("  3) Hard   (1-1000, 10 attempts)")
    choice = input("Select 1-3 (default 2): ").strip()
    if choice == "1":
        return (1, 20, 7, "Easy")
    if choice == "3":
        return (1, 1000, 10, "Hard")
    return (1, 100, 8, "Normal")


def give_hint(secret, guess, attempts_left):
    diff = abs(secret - guess)
    if diff == 0:
        return "Correct!"
    if diff <= max(1, secret * 0.02):
        return "Extremely close!"
    if diff <= 2:
        return "Very close!"
    if diff <= 10:
        return "Close!"
    # Directional hint with attempts left consideration
    dir_hint = "higher" if guess < secret else "lower"
    if attempts_left <= 2:
        return f"Try {dir_hint} (final hints)."
    return f"{dir_hint.capitalize()} than {guess}."


def play_round():
    low, high, attempts_allowed, label = choose_difficulty()
    secret = random.randint(low, high)
    attempts = 0
    start_time = time.time()
    print(f"\nI've picked a number between {low} and {high}. You have {attempts_allowed} attempts. Good luck!")

    while attempts < attempts_allowed:
        attempts += 1
        try:
            guess = int(input(f"[{attempts}/{attempts_allowed}] Your guess: ").strip())
        except ValueError:
            print("Please enter an integer.")
            attempts -= 1
            continue

        if guess == secret:
            duration = time.time() - start_time
            score = max(0, (high - low + 1) - (attempts - 1)) + int(max(0, (attempts_allowed - attempts) * 2))
            print(f"Correct! The number was {secret}. Attempts: {attempts}. Time: {duration:.1f}s. Score: {score}.")
            return {"won": True, "attempts": attempts, "time": duration, "score": score, "difficulty": label}
        else:
            hint = give_hint(secret, guess, attempts_allowed - attempts)
            print(f"Wrong. Hint: {hint}")

    print(f"\nOut of attempts. The number was {secret}. Better luck next time.")
    return {"won": False, "attempts": attempts_allowed, "time": time.time() - start_time, "score": 0, "difficulty": label}


def main():
    print("Number Wizard — Guess the number game")
    hs = load_highscores()
    plays = hs.get("plays", 0)
    best = hs.get("best_score", None)

    while True:
        result = play_round()
        plays += 1
        if result["won"] and (best is None or result["score"] > best["score"]):
            best = {"score": result["score"], "attempts": result["attempts"], "time": result["time"], "difficulty": result["difficulty"], "when": time.time()}
            print("New high score!")
        print(f"Session result: {'Win' if result['won'] else 'Loss'} | Score: {result['score']} | Difficulty: {result['difficulty']}")
        print(f"Total plays: {plays}")
        if best:
            print(f"Best score: {best['score']} (diff {best['difficulty']}, attempts {best['attempts']})")

        hs_out = {"best_score": best, "plays": plays}
        save_highscores(hs_out)

        again = input("\nPlay again? (Y/n) ").strip().lower()
        if again not in ("", "y", "yes"):
            print("Thanks for playing. Goodbye.")
            break


if __name__ == "__main__":
    main()