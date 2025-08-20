# src/datagen/view_game.py
import os
import time
from pathlib import Path
import argparse
import sys

# Cross-platform single keypress
if os.name == "nt":
    import msvcrt

    def get_key():
        return msvcrt.getch().decode("utf-8").lower()
else:
    import tty
    import termios

    def get_key():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            key = sys.stdin.read(1).lower()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return key


def parse_args():
    parser = argparse.ArgumentParser(description="Animate Minesweeper solver steps interactively.")
    parser.add_argument("--game", type=int, default=0, help="Game index to view (default: 0)")
    parser.add_argument("--speed", type=float, default=1.0, help="Step delay in seconds (default: 1.0)")
    return parser.parse_args()


def print_board_diff(prev, curr, paused: bool):
    os.system("cls" if os.name == "nt" else "clear")
    header = "[PAUSED]" if paused else "[PLAYING]"
    print(f"{header}\n")
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
    print("\n[Controls] a=prev, d=next, x=pause/resume, q=quit")


def main():
    args = parse_args()
    game_index = args.game
    step_delay = args.speed

    base_dir = Path(__file__).parent.parent.parent.resolve()
    game_dir = base_dir / "data" / f"game{game_index}"

    if not game_dir.exists():
        print(f"[ERROR] Game directory {game_dir} does not exist!")
        return

    step_files = sorted(game_dir.glob("step*.txt"), key=lambda p: int(p.stem[4:]))
    steps = []
    for step_file in step_files:
        with open(step_file, "r") as f:
            steps.append([list(line.strip()) for line in f.readlines()])

    step_index = 0
    paused = False
    while True:
        prev_board = steps[step_index - 1] if step_index > 0 else None
        print_board_diff(prev_board, steps[step_index], paused)

        start_time = time.time()
        while True:
            key = None
            if os.name == "nt" and msvcrt.kbhit():
                key = get_key()
            elif os.name != "nt":
                import select
                dr, _, _ = select.select([sys.stdin], [], [], 0.1)
                if dr:
                    key = get_key()

            if key:
                if key == "a":
                    step_index = max(0, step_index - 1)
                    paused = True  # auto pause on manual move
                    break
                elif key == "d":
                    step_index = min(len(steps) - 1, step_index + 1)
                    paused = True  # auto pause on manual move
                    break
                elif key == "x":
                    paused = not paused
                    break  # immediately update display
                elif key == "q":
                    os.system("cls" if os.name == "nt" else "clear")
                    print("Exiting...")
                    return

            if not paused and time.time() - start_time >= step_delay:
                step_index += 1
                if step_index >= len(steps):
                    step_index = len(steps) - 1
                    paused = True  # auto pause at last step
                break


if __name__ == "__main__":
    main()
