# src/datagen/datagen.py
import os
from pathlib import Path
from typing import Optional
from src.minesweeper.validboard import ValidBoard
from src.minesweeper.minesweepersolver import MinesweeperSolver
import random
import shutil


class DataGenerator:
    def __init__(self, output_dir: str = "../../data"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.game_counter = self._get_next_game_index()

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
        # Randomize number of mines between 10 and 16
        mines = random.randint(10, 16)
        vb = ValidBoard(rows=8, cols=8, mines=mines)

        # Make first move somewhere safe (center)
        vb.reveal(4, 4)

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

        # Solve the board step by step
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

        # Save final hidden board
        hidden_file = game_folder / "hidden_state.txt"
        with open(hidden_file, "w") as f:
            for row in vb.board.hidden_board:
                f.write(" ".join(str(cell) for cell in row) + "\n")

        self.game_counter += 1
        print(f"Saved game {game_folder.resolve()} with {len(step_states)} solver steps.")


if __name__ == "__main__":
    generator = DataGenerator()
    generator.generate_games(num_games=3)  # generate 3 sample games
