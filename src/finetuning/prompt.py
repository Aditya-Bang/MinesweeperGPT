# src/finetuning/prompt.py
from src.globals import TRAINING_ROWS, TRAINING_COLS
from src.models import MinesweeperExample

REASONING_START = "<think>"
REASONING_END   = "</think>"
SOLUTION_START  = "<SOLUTION>"
SOLUTION_END    = "</SOLUTION>"

SYSTEM_PROMPT = f"""You are a Minesweeper assistant.
The game board is always {TRAINING_ROWS}x{TRAINING_COLS} in size.
You will be given the current board state.
Your task is to suggest exactly one next move.

Moves must be in the format:
- 'row col'   → to reveal a cell
- 'row col f' → to flag a cell as a mine

Constraints:
- Row values are integers in the range [1-{TRAINING_ROWS}].
- Column values are integers in the range [1-{TRAINING_COLS}].
- Only provide one move, not multiple.
- Think carefully about the board and explain your reasoning between {REASONING_START} and {REASONING_END}.
- Then, provide only the move between {SOLUTION_START} and {SOLUTION_END}.
"""

def format_example(example: MinesweeperExample) -> dict:
    return {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": example.input},
            {"role": "assistant", "content": example.action},
        ]
    }
