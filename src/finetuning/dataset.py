# src/finetuning/dataset.py
from pathlib import Path
from src.utils import get_base_directory
from src.models import MinesweeperExample
from typing import List
import random


class MinesweeperDataset:
    def __init__(self, data_dir: str = "data"):
        self.base_dir: Path = get_base_directory()
        self.data_dir: Path = (self.base_dir / data_dir).resolve()
        print(f"Using data directory: {self.data_dir}")
        if not self.data_dir.exists():
            print(f"Data directory does not exist: {self.data_dir}")
        else:
            print(f"Data directory exists: {self.data_dir}")
        self.games = sorted([g for g in self.data_dir.glob("game*") if g.is_dir()])
        if not self.games:
            print(f"No game directories found in {self.data_dir}")
        else:
            print(f"Found {len(self.games)} game directories in {self.data_dir}")

    def load_examples(self) -> List[MinesweeperExample]:
        examples: List[MinesweeperExample] = []
        for game in self.games:
            step_files = sorted(game.glob("step*.txt"), key=lambda p: int(p.stem[4:]))
            hidden_state = (game / "hidden_state.txt").read_text().splitlines()

            for i in range(len(step_files) - 1):
                state = step_files[i].read_text()
                next_state = step_files[i+1].read_text()

                # Find action: difference between states
                action = self._extract_action(state, next_state)
                examples.append({"input": state, "action": action, "hidden_state": hidden_state})
        random.shuffle(examples)
        return examples

    def _extract_action(self, prev_state: str, next_state: str) -> str:
        prev_lines = prev_state.splitlines()
        next_lines = next_state.splitlines()
        for r, (pl, nl) in enumerate(zip(prev_lines, next_lines)):
            for c, (pc, nc) in enumerate(zip(pl, nl)):
                if pc != nc:
                    return f"{r} {c}" if nc != "F" else f"{r} {c} f"
        raise ValueError("No difference found between states; every state transition must have a difference.")
