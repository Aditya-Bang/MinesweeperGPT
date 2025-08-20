# tests/minesweeper/datamanual.py
from src.minesweeper.validboard import ValidBoard
from src.minesweeper.minesweepersolver import MinesweeperSolver


vb = ValidBoard(rows=8, cols=8, mines=12)
first_reveal = vb.reveal(4, 4)
solver = MinesweeperSolver(vb.board)
solver.solve()

vb.print_board(reveal_hidden=False)
vb.print_board(reveal_hidden=True)

for r in range(vb.rows):
    for c in range(vb.cols):
        if vb.board.board[r][c] == 'F':
            assert vb.board.hidden_board[r][c] == 'M', f"Flag at ({r},{c}) is not a mine!"

print("All clear")
