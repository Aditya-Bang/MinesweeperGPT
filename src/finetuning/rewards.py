# src/finetuning/rewards.py
import re
from typing import List, Optional, Tuple, Dict

from src.globals import TRAINING_ROWS, TRAINING_COLS


def is_output_valid(move_str: str) -> Optional[Tuple[int, int, str]]:
    """
    Check if the output move string matches the expected format.
    """
    return re.match(r"row:\s*(\d+),\s*col:\s*(\d+),\s*action:\s*(reveal|flag)", move_str.strip())


def parse_move(move_str: str) -> Tuple[Optional[int], Optional[int], Optional[str]]:
    """
    Parse a move string of the format: "row: NUM, col: NUM, action: reveal/flag"
    Returns a tuple: (row, col, action)
    """
    match = is_output_valid(move_str)
    if match:
        row, col, action = match.groups()
        return int(row) - 1, int(col) - 1, action  # Convert to 0-indexed
    return None, None, None


def move_square_in_bounds(row: int, col: int) -> bool: # row, col 0-indexed
    """
    Check if the given row and column are within the board bounds.
    """
    return 0 <= row < TRAINING_ROWS and 0 <= col < TRAINING_COLS



def reward_format_correct(completions: List[List[Dict[str, str]]], **kwargs) -> List[float]:
    """
    Reward 1: Check if the move follows the correct format.
    """
    responses = [completion[0]["content"] for completion in completions]
    return [1.0 if is_output_valid(response) else 0.0 for response in responses]


def reward_valid_cell(completions: List[List[Dict[str, str]]], hidden_state: List[List[str]], **kwargs) -> List[float]:
    """
    Reward 2: Reward if the move targets an unrevealed cell ('*').
    board: List of strings representing the current board state.
    """
    scores = []
    responses = [completion[0]["content"] for completion in completions]
    for response in responses:
        row, col, action = parse_move(response)
        if row is None:
            scores.append(0.0)
            continue
        if not move_square_in_bounds(row, col):
            scores.append(0.0)
            continue
        if hidden_state[0][row][col] == '*':
            scores.append(2.0)
            continue
        scores.append(0.0)
    return scores


def reward_correct_move(completions: List[List[Dict[str, str]]], hidden_state: List[List[str]], **kwargs) -> List:
    """
    Reward 3: Reward if the move reveals an empty square (0) or flags a mine correctly.
    hidden_state: List of strings representing the ground truth board with mines.
    """
    scores = []
    responses = [completion[0]["content"] for completion in completions]
    for response in responses:
        row, col, action = parse_move(response)
        if row is None:
            scores.append(0.0)
            continue

        if action == "reveal":
            # Correctly revealing an empty square
            scores.append(2.0 if hidden_state[row][col] != 'M' else 0.0)
        elif action == "flag":
            # Correctly flagging a mine
            scores.append(2.0 if hidden_state[row][col] == '*' and hidden_state[row][col] == 'M' else 0.0)
    return scores


# def total_reward(move: str, board: List[str], hidden_state: List[str]) -> float:
#     """
#     Combine all reward functions with optional weighting.
#     """
#     r1 = reward_format_correct(move)
#     r2 = reward_valid_cell(move, board)
#     r3 = reward_correct_move(move, board, hidden_state)

#     # You can tune weights here if needed
#     return r1 + r2 + r3
