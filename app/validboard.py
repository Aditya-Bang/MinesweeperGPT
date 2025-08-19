# app/game.py
from app.board import Board
from app.minesweepersolver import MinesweeperSolver


class ValidBoard:
    def __init__(self, rows=8, cols=8, mines=10):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.board = None
        self.first_move_done = False

    def first_move(self, r: int, c: int):
        """
        Generate a valid board only after the first move.
        Ensures first click is safe and solvable.
        """
        while True:
            board = Board(self.rows, self.cols, self.mines)
            board.generate_random_board(first_click=(r, c))
            solver = MinesweeperSolver(board)
            if solver.is_solvable() and board.hidden_board[r][c] == 0:
                self.board = board
                self.first_move_done = True
                break

        return self.board.reveal(r, c)

    def reveal(self, r: int, c: int):
        if not self.first_move_done:
            return self.first_move(r, c)
        return self.board.reveal(r, c)

    def check_win(self):
        return self.board.check_win() if self.board else False

    def print_board(self, reveal_hidden=False):
        if self.board:
            self.board.print_board(reveal_hidden)
        else:
            print("Board not initialized yet.")
