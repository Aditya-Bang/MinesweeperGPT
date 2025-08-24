# src/finetuning/rewards.py
import re
from typing import List, Optional, Tuple, Dict

from src.globals import TRAINING_ROWS, TRAINING_COLS

global PRINTED_TIMES
PRINTED_TIMES = 0
global PRINT_EVERY_STEPS
PRINT_EVERY_STEPS = 5


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



def reward_format_correct(
        completions: List[List[Dict[str, str]]],
        **kwargs
    ) -> List[float]:
    """
    Reward 1: Check if the move follows the correct format.
    """
    responses = [completion[0]["content"] for completion in completions]
    return [1.0 if is_output_valid(response) else 0.0 for response in responses]


def reward_valid_cell(
        completions: List[List[Dict[str, str]]],
        board_state: List[List[List[str]]],
        **kwargs
    ) -> List[float]:
    """
    Reward 2: Reward if the move targets an unrevealed cell ('*').
    board: List of strings representing the current board state.
    """
    scores = []
    responses = [completion[0]["content"] for completion in completions]
    for response, b_state in zip(responses, board_state):
        row, col, action = parse_move(response)
        if row is None:
            scores.append(0.0)
            continue
        if not move_square_in_bounds(row, col):
            scores.append(0.0)
            continue
        if b_state[row][col] == '*':
            scores.append(2.0)
            continue
        scores.append(0.0)
    return scores

def reward_logical_move(
        prompts: List[List[Dict[str, str]]],
        completions: List[List[Dict[str, str]]],
        board_state: List[List[List[str]]],
        hidden_state: List[List[List[str]]],
        **kwargs
    ) -> List[float]:
    """
    Reward 3: Give score if the move is logical.
    A move is rewarded (score=3) if the chosen square is unrevealed ('*')
    AND at least one of the 8 surrounding squares is revealed (not '*').
    """
    scores = []
    responses = [completion[0]["content"] for completion in completions]

    # directions for 8 neighbors
    neighbors = [(-1, -1), (-1, 0), (-1, 1),
                 (0, -1),           (0, 1),
                 (1, -1),  (1, 0),  (1, 1)]

    for response, b_state, h_state in zip(responses, board_state, hidden_state):
        row, col, action = parse_move(response)
        if row is None or not move_square_in_bounds(row, col):
            scores.append(0.0)
            continue

        # must be unrevealed
        if b_state[row][col] != '*':
            scores.append(0.0)
            continue

        # check surrounding squares
        logical = 0
        for dr, dc in neighbors:
            nr, nc = row + dr, col + dc
            if move_square_in_bounds(nr, nc):
                if b_state[nr][nc] != '*':
                    logical += 1

        scores.append(min(float(logical), 3.0))

    return scores

def reward_correct_move(
        prompts: List[List[Dict[str, str]]],
        completions: List[List[Dict[str, str]]],
        board_state: List[List[List[str]]],
        hidden_state: List[List[List[str]]],
        **kwargs
    ) -> List[float]:
    """
    Reward 4: Reward if the move reveals an empty square or flags a mine correctly.
    Additional rule: If the move is not logical (none of the surrounding squares
    is a number or 'F'), then reward = 0.
    
    hidden_state: List of strings representing the ground truth board with mines.
    """
    scores = []
    responses = [completion[0]["content"] for completion in completions]

    global PRINTED_TIMES
    global PRINT_EVERY_STEPS
    if PRINTED_TIMES % PRINT_EVERY_STEPS == 0:
        print(
            '*'*20 + f" Reward 4 Debugging Info (every {PRINT_EVERY_STEPS} steps) " + '*'*20 + '\n' +
            f"Prompt:\n{prompts[0][-1]['content']}\n" +
            f"Responses:\n{responses[0]}\n"
        )
    PRINTED_TIMES += 1

    # directions for 8 neighbors
    neighbors = [(-1, -1), (-1, 0), (-1, 1),
                 (0, -1),           (0, 1),
                 (1, -1),  (1, 0),  (1, 1)]

    for response, b_state, h_state in zip(responses, board_state, hidden_state):
        row, col, action = parse_move(response)
        if row is None or not move_square_in_bounds(row, col):
            scores.append(0.0)
            continue
        if b_state[row][col] != '*':
            scores.append(0.0)
            continue

        # Check if move is "logical"
        logical = False
        for dr, dc in neighbors:
            nr, nc = row + dr, col + dc
            if move_square_in_bounds(nr, nc):
                neighbor_val = b_state[nr][nc]
                if neighbor_val.isdigit() or neighbor_val == "F":
                    logical = True
                    break

        if not logical:
            scores.append(0.0)
            continue

        # Only reward logical AND correct moves
        if action == "reveal":
            scores.append(5.0 if h_state[row][col] != 'M' else 0.0)
        elif action == "flag":
            scores.append(5.0 if h_state[row][col] == 'M' else 0.0)
        else:
            scores.append(0.0)

    return scores
