from src.minesweeper.validboard import ValidBoard

vb = ValidBoard(rows=8, cols=8, mines=10)
first_reveal = vb.reveal(0, 0)

vb.print_board(reveal_hidden=False)
vb.print_board(reveal_hidden=True)  # Debug: see mines