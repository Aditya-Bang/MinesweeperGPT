# src/datagen/view_game.py
import os
import time
from pathlib import Path

# ---------------- Config ----------------
GAME_INDEX = 0       # which game to view
STEP_DELAY = 3     # seconds between steps
# ----------------------------------------

# Compute project root relative to this file
BASE_DIR = Path(__file__).parent.parent.parent.resolve()
GAME_DIR = BASE_DIR / "data" / f"game{GAME_INDEX}"

# Load all step files in order
STEP_FILES = sorted(GAME_DIR.glob("step*.txt"), key=lambda p: int(p.stem[4:]))

def print_board_diff(prev, curr):
    os.system("cls" if os.name == "nt" else "clear")
    for r in range(len(curr)):
        line_str = ""
        for c in range(len(curr[r])):
            prev_cell = prev[r][c] if prev else None
            curr_cell = curr[r][c]

            if curr_cell != prev_cell:
                if curr_cell == "F":
                    line_str += f"\033[93m{curr_cell}\033[0m "  # yellow for flags
                else:
                    line_str += f"\033[92m{curr_cell}\033[0m "  # green for revealed
            else:
                line_str += f"{curr_cell} "
        print(line_str)
    print("\n")  # extra spacing

prev_board = None
for step_file in STEP_FILES:
    with open(step_file, "r") as f:
        curr_board = [list(line.strip()) for line in f.readlines()]

    print_board_diff(prev_board, curr_board)
    time.sleep(STEP_DELAY)
    prev_board = curr_board
