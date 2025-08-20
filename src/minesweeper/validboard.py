# src/minesweeper/valid_board.py
from src.minesweeper.board import Board
from src.minesweeper.minesweepersolver import MinesweeperSolver

# MAX_BOARD_CREATION_ATTEMPTS = 10000

class ValidBoard:
    def __init__(self, rows=8, cols=8, mines=16):
        if mines >= rows * cols:
            raise ValueError("Number of mines must be less than total board spaces to allow at least one empty square.")
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.board = None
        self.first_move_done = False

    def first_move(self, r: int, c: int) -> bool:
        """
        Generate a valid board only after the first move.
        Ensures first click reveals a 0 and that the board is solvable.
        """
        # for _ in range(MAX_BOARD_CREATION_ATTEMPTS):
        while True:
            board = Board(self.rows, self.cols, self.mines)
            board.generate_random_board()

            # Reveal the first clicked cell
            alive = board.reveal(r, c)
            if not alive:
                continue  # shouldn't happen since we avoid mine on first click

            # Ensure it's a 0
            if board.hidden_board[r][c] != 0:
                continue

            # copy constructor
            solver_board = Board(
                rows=board.rows,
                cols=board.cols,
                mines=board.mines,
                board_data=board.board,
                hidden_data=board.hidden_board
            )

            # Pass the partially revealed board to solver
            solver = MinesweeperSolver(solver_board)
            if solver.is_solvable():
                self.board = board
                self.first_move_done = True
                break
        # else:
        #     raise RuntimeError(f"Failed to generate a valid board after {MAX_BOARD_CREATION_ATTEMPTS} attempts.")

        return True

    def reveal(self, r: int, c: int) -> bool:
        if not self.first_move_done:
            return self.first_move(r, c)
        return self.board.reveal(r, c)
    
    def flag(self, r: int, c: int) -> None:
        if self.board:
            self.board.flag(r, c)

    def check_win(self) -> bool:
        return self.board.check_win() if self.board else False

    def print_board(self, reveal_hidden=False):
        if self.board:
            self.board.print_board(reveal_hidden)
        else:
            # Print a board of all '*' if not initialized
            board_to_print = [['*' for _ in range(self.cols)] for _ in range(self.rows)]
            for row in board_to_print:
                print(" ".join(str(cell) for cell in row))
            print()
