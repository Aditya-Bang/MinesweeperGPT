# board.py

import random
from collections import deque

class Board:
    def __init__(self, rows: int = 8, cols: int = 8, mines: int = 10):
        self.rows: int = rows
        self.cols: int = cols
        self.mines: int = mines
        self.reset_board()
    
    def reset_board(self):
        self.board = [["*" for _ in range(self.cols)] for _ in range(self.rows)]
        self.hidden_board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def generate_random_board(self):
        self.reset_board()

        # Place mines randomly
        positions = set()
        while len(positions) < self.mines:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            positions.add((r, c))
        for r, c in positions:
            self.hidden_board[r][c] = "M"

        # Fill numbers for non-mine cells
        for r in range(self.rows):
            for c in range(self.cols):
                if self.hidden_board[r][c] == "M":
                    continue
                count = 0
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < self.rows and 0 <= nc < self.cols:
                            if self.hidden_board[nr][nc] == "M":
                                count += 1
                self.hidden_board[r][c] = count

    def reveal(self, r: int, c: int) -> bool:
        """
        Reveal a cell. Returns False if a mine is hit, True otherwise.
        """
        if self.board[r][c] != "*":
            return True  # already revealed

        if self.hidden_board[r][c] == "M":
            self.board[r][c] = "M"
            return False  # Mine hit, game over

        # Flood-fill with BFS for 0s
        queue = deque([(r, c)])
        while queue:
            cr, cc = queue.popleft()
            if self.board[cr][cc] != "*":
                continue  # already revealed

            val = self.hidden_board[cr][cc]
            self.board[cr][cc] = str(val) if val > 0 else " "

            if val == 0:
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = cr + dr, cc + dc
                        if 0 <= nr < self.rows and 0 <= nc < self.cols:
                            if self.board[nr][nc] == "*":
                                queue.append((nr, nc))
        return True

    def print_board(self, reveal_hidden=False):
        board_to_print = self.hidden_board if reveal_hidden else self.board
        for row in board_to_print:
            print(" ".join(str(cell) for cell in row))
        print()
