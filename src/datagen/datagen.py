# src/datagen/datagen.py
from pathlib import Path
from typing import Optional
from src.minesweeper.validboard import ValidBoard
from src.minesweeper.minesweepersolver import MinesweeperSolver
from src.globals import TRAINING_ROWS, TRAINING_COLS, TRAINING_MIN_MINES, TRAINING_MAX_MINES
from src.utils import get_base_directory
import random
import shutil


class DataGenerator:
    def __init__(self, output_dir: str = "data/train"):
        # Go two levels up from this file
        self.base_dir: Path = get_base_directory()
        self.output_dir: Path = (self.base_dir / output_dir).resolve()
        self.output_dir.mkdir(parents=True, exist_ok=True)
        print(f"[INFO] Storing game data in: {self.output_dir}")

        self.game_counter: int = self._get_next_game_index()

    def _get_next_game_index(self) -> int:
        """
        Determines the next game folder index (game0, game1, etc.)
        """
        existing = [d.name for d in self.output_dir.iterdir() if d.is_dir() and d.name.startswith("game")]
        indices = [int(d[4:]) for d in existing if d[4:].isdigit()]
        return max(indices, default=-1) + 1

    def generate_games(self, num_games: int = 1):
        """
        Generate multiple random games and store their solver steps
        """
        for _ in range(num_games):
            self._generate_single_game()

    def _generate_single_game(self):
        mines = random.randint(TRAINING_MIN_MINES, TRAINING_MAX_MINES)
        vb = ValidBoard(rows=TRAINING_ROWS, cols=TRAINING_COLS, mines=mines)

        # Random first move location
        first_r = random.randint(0, TRAINING_ROWS - 1)
        first_c = random.randint(0, TRAINING_COLS - 1)
        vb.reveal(first_r, first_c)

        solver = MinesweeperSolver(vb.board)
        step_states = []

        # Monkey-patch board.print_board to capture intermediate states
        original_print = vb.board.print_board

        def capture_board(reveal_hidden: Optional[bool] = False):
            from io import StringIO
            import sys

            buf = StringIO()
            sys.stdout = buf
            original_print(reveal_hidden)
            sys.stdout = sys.__stdout__
            step_states.append(buf.getvalue())

        vb.board.print_board = capture_board
        solver.solve(verbose=True)

        # Save game folder
        game_folder = self.output_dir / f"game{self.game_counter}"
        if game_folder.exists():
            shutil.rmtree(game_folder)
        game_folder.mkdir(parents=True, exist_ok=True)

        # Save all step files
        for i, state in enumerate(step_states):
            step_file = game_folder / f"step{i}.txt"
            with open(step_file, "w") as f:
                f.write(state)

        # Save hidden board state
        hidden_file = game_folder / "hidden_state.txt"
        with open(hidden_file, "w") as f:
            for row in vb.board.hidden_board:
                f.write(" ".join(str(cell) for cell in row) + "\n")

        # Save metadata
        metadata_file = game_folder / "metadata.txt"
        with open(metadata_file, "w") as f:
            f.write(f"rows: {vb.rows}\n")
            f.write(f"cols: {vb.cols}\n")
            f.write(f"mines: {vb.mines}\n")
            f.write(f"start_row: {first_r+1}\n")
            f.write(f"start_col: {first_c+1}\n")

        self.game_counter += 1
        print(f"[INFO] Saved game {self.game_counter} to: {game_folder.resolve()} with {len(step_states)} solver steps.")


if __name__ == "__main__":
    generator = DataGenerator()
    generator.generate_games(num_games=10)
