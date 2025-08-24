# src/finetuning/dataset.py
from pathlib import Path
from typing import List, Dict, Any
import random

from src.utils import get_base_directory
from src.models import MinesweeperExample
from src.finetuning.prompt import format_example
from datasets import Dataset


class MinesweeperDatasetLoader:
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
                state_str = step_files[i].read_text()
                board_state: List[str] = state_str.splitlines()
                # next_state = step_files[i+1].read_text()

                # Find action: difference between states (TODO: store all possible valid actions)
                # action = self._extract_action(state, next_state)
                examples.append(MinesweeperExample(input=state_str, board_state=board_state, hidden_state=hidden_state))
        random.shuffle(examples)
        return examples

    # def _extract_action(self, prev_state: str, next_state: str) -> str:
    #     prev_lines = prev_state.splitlines()
    #     next_lines = next_state.splitlines()
    #     for r, (pl, nl) in enumerate(zip(prev_lines, next_lines)):
    #         for c, (pc, nc) in enumerate(zip(pl, nl)):
    #             if pc != nc:
    #                 return f"{r} {c}" if nc != "F" else f"{r} {c} f"
    #     raise ValueError("No difference found between states; every state transition must have a difference.")

    def to_hf_dataset(self) -> Dataset:
        """
        Convert Minesweeper examples to a Hugging Face Dataset object
        suitable for GRPO training.
        """
        examples: List[MinesweeperExample] = self.load_examples()

        hf_data: List[Dict[str, Any]] = [
            {
                **format_example(ex),
                "board_state": ex.board_state,
                "hidden_state": ex.hidden_state,
            }
            for ex in examples
        ]

        return Dataset.from_list(hf_data)
