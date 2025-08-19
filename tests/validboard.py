# tests/test_valid_board.py
import pytest
from app.validboard import ValidBoard


def test_first_move_reveals_zero_and_board_is_solvable():
    vb = ValidBoard(rows=8, cols=8, mines=10)

    # Make the first move at (0, 0)
    first_reveal = vb.reveal(0, 0)

    # Board should now be initialized
    assert vb.board is not None, "Board should be initialized after first move"

    # First revealed cell must be 0
    assert vb.board.hidden_board[0][0] == 0, "First revealed square should be 0"

    # First move should not hit a mine
    assert first_reveal is True, "First move should not hit a mine"

    # Board should be solvable (solver should confirm)
    from app.minesweepersolver import MinesweeperSolver
    solver = MinesweeperSolver(vb.board)
    assert solver.is_solvable() is True, "Board should be solvable deterministically"


def test_reveal_updates_board_and_check_win():
    vb = ValidBoard(rows=5, cols=5, mines=3)

    # First move to initialize the board
    vb.reveal(0, 0)

    # Reveal a safe square
    result = vb.reveal(0, 1)
    assert result is True, "Revealing a safe square should return True"

    # Check that the board is not already won (most likely)
    assert vb.check_win() is False, "Board should not be won immediately after first move"

    # Reveal all non-mine squares to simulate winning
    for r in range(vb.rows):
        for c in range(vb.cols):
            if vb.board.hidden_board[r][c] != "M":
                vb.reveal(r, c)

    # Now check_win should return True
    assert vb.check_win() is True, "Board should be won after revealing all non-mine squares"
