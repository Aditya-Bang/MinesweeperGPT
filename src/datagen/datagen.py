# src/datagen/datagen.py
from src.minesweeper.validboard import ValidBoard
from src.minesweeper.minesweepersolver import MinesweeperSolver

vb = ValidBoard(rows=8, cols=8, mines=16)
first_reveal = vb.reveal(4, 4)
solver = MinesweeperSolver(vb.board)
solver.solve(verbose=True)
