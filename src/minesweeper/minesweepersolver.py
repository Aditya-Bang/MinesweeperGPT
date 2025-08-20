# src/minesweeper/solver.py
from __future__ import annotations
from typing import List, Tuple
from src.minesweeper.board import Board


class MinesweeperSolver:
    def __init__(self, board: Board):
        self.board: Board = board

    def is_solvable(self) -> bool:
        """
        Determines if the current board can be solved deterministically
        (without guessing). Works on partially revealed boards.
        """
        return self.solve()

    def solve(self) -> bool:
        """
        Deterministically solve the board step by step:
        - Reveals safe squares
        - Flags certain mines
        Returns True if fully solved, False otherwise.
        """
        progress = True

        while progress:
            progress = False
            for r in range(self.board.rows):
                for c in range(self.board.cols):
                    cell = self.board.board[r][c]

                    # Skip unrevealed, empty, flagged, or mines
                    if cell in ("*", " ", "M", "F"):
                        continue

                    num = int(cell)
                    hidden_neighbors, flagged_count = self._get_neighbors(r, c)

                    # Rule 1: all mines flagged → remaining hidden neighbors are safe
                    if flagged_count == num and hidden_neighbors:
                        for hr, hc in hidden_neighbors:
                            if self.board.board[hr][hc] == "*":
                                self.board.reveal(hr, hc)
                                progress = True

                    # Rule 2: all hidden neighbors are mines
                    elif flagged_count + len(hidden_neighbors) == num and hidden_neighbors:
                        for hr, hc in hidden_neighbors:
                            if self.board.board[hr][hc] == "*":
                                self.board.flag(hr, hc)
                                progress = True

            # Board completely solved?
            if self.board.check_win():
                return True

        # No deterministic moves left, but not solved → requires guessing
        return False

    def _get_neighbors(self, r: int, c: int) -> Tuple[List[Tuple[int, int]], int]:
        """
        Returns a tuple (hidden_neighbors, flagged_count) for a given cell.
        """
        hidden: List[Tuple[int, int]] = []
        flagged: int = 0

        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.board.rows and 0 <= nc < self.board.cols:
                    neighbor = self.board.board[nr][nc]
                    if neighbor == "*":
                        hidden.append((nr, nc))
                    elif neighbor == "F":
                        flagged += 1

        return hidden, flagged
