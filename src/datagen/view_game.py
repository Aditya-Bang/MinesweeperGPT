# src/datagen/view_game.py
import os
import time
from pathlib import Path
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Animate Minesweeper solver steps.")
    parser.add_argument("--game", type=int, default=0, help="Game index to view (default: 0)")
    parser.add_argument("--speed", type=float, default=3.0, help="Step delay in seconds (default: 3.0)")
    return parser.parse_args()

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

def main():
    args = parse_args()
    game_index = args.game
    step_delay = args.speed

    # Compute project root relative to this file
    base_dir = Path(__file__).parent.parent.parent.resolve()
    game_dir = base_dir / "data" / f"game{game_index}"

    if not game_dir.exists():
        print(f"[ERROR] Game directory {game_dir} does not exist!")
        return

    step_files = sorted(game_dir.glob("step*.txt"), key=lambda p: int(p.stem[4:]))

    prev_board = None
    for step_file in step_files:
        with open(step_file, "r") as f:
            curr_board = [list(line.strip()) for line in f.readlines()]

        print_board_diff(prev_board, curr_board)
        time.sleep(step_delay)
        prev_board = curr_board

if __name__ == "__main__":
    main()
