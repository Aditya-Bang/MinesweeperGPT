# app/minesweeper.py
from app.validboard import ValidBoard


class Minesweeper:
    def __init__(self, rows: int = 8, cols: int = 8, mines: int = 10):
        self.valid_board = ValidBoard(rows, cols, mines)
        self.game_over = False

    def play(self) -> None:
        """
        Run the interactive Minesweeper game loop until win or loss.
        """
        print("Welcome to Minesweeper!")
        self.valid_board.print_board()

        while not self.game_over:
            command = input("Enter move (r c [f for flag]): ").strip().lower()
            parts = command.split()

            if len(parts) < 2:
                print("Invalid input. Format: row col [f]")
                continue

            try:
                r = int(parts[0])-1
                c = int(parts[1])-1
            except ValueError:
                print("Row and column must be integers.")
                continue

            if not (0 <= r < self.valid_board.rows and 0 <= c < self.valid_board.cols):
                print("Coordinates out of bounds.")
                continue

            # Check if player wants to flag
            flag = len(parts) == 3 and parts[2] == "f"

            if flag:
                # Simple toggle flag
                self.valid_board.flag(r, c)
            else:
                alive = self.valid_board.reveal(r, c)
                if not alive:
                    self.game_over = True
                    print("💥 BOOM! You hit a mine. Game Over!")
                    self.valid_board.print_board(reveal_hidden=True)
                    break

            # Print board after move
            self.valid_board.print_board()

            # Check for win
            if self.valid_board.check_win():
                self.game_over = True
                print("🎉 Congratulations! You cleared all the mines!")
                self.valid_board.print_board(reveal_hidden=True)
                break
