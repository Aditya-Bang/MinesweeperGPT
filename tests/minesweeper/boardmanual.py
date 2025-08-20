from src.minesweeper.board import Board

b = Board()
b.generate_random_board()
b.print_board(reveal_hidden=True)   # Debug: see mines

alive = b.reveal(0, 0)
b.print_board()

if not alive:
    print("💥 You hit a mine!")
elif b.check_win():
    print("🎉 You won!")
