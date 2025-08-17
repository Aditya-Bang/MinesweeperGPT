# minesweeper.py

import random

class Minesweeper:
    def __init__(self, size=8, num_mines=10):
        self.size = size
        self.num_mines = num_mines
        self.board = [['*' for _ in range(size)] for _ in range(size)]  # display board
        self.hidden_board = [[0 for _ in range(size)] for _ in range(size)]  # actual values
        self.revealed = [[False for _ in range(size)] for _ in range(size)]
        self.flags = [[False for _ in range(size)] for _ in range(size)]
        self._place_mines()
        self._compute_numbers()

    def _place_mines(self):
        mines = 0
        while mines < self.num_mines:
            r, c = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            if self.hidden_board[r][c] != "M":
                self.hidden_board[r][c] = "M"
                mines += 1

    def _compute_numbers(self):
        directions = [(-1,-1), (-1,0), (-1,1),
                      (0,-1),         (0,1),
                      (1,-1), (1,0),  (1,1)]
        for r in range(self.size):
            for c in range(self.size):
                if self.hidden_board[r][c] == "M":
                    continue
                count = 0
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.size and 0 <= nc < self.size and self.hidden_board[nr][nc] == "M":
                        count += 1
                self.hidden_board[r][c] = count

    def print_board(self):
        print("\n   " + " ".join(str(i+1) for i in range(self.size)))
        print("   " + "--"*self.size)
        for i, row in enumerate(self.board):
            print(f"{i+1:2}| " + " ".join(row))
        print()

    def reveal(self, r, c):
        if self.flags[r][c]:
            print("Tile is flagged, unflag first.")
            return False
        if self.revealed[r][c]:
            return False
        self.revealed[r][c] = True
        val = self.hidden_board[r][c]
        if val == "M":
            self.board[r][c] = "X"
            print("💥 You hit a mine! Game over.")
            return True  # game over
        self.board[r][c] = str(val)
        if val == 0:
            self.board[r][c] = "0"
            # reveal neighbors recursively
            directions = [(-1,-1), (-1,0), (-1,1),
                          (0,-1),         (0,1),
                          (1,-1), (1,0),  (1,1)]
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.size and 0 <= nc < self.size:
                    if not self.revealed[nr][nc]:
                        self.reveal(nr, nc)
        return False

    def flag(self, r, c):
        if self.revealed[r][c]:
            print("Tile already revealed.")
            return
        self.flags[r][c] = not self.flags[r][c]
        self.board[r][c] = "F" if self.flags[r][c] else "*"

    def check_win(self):
        for r in range(self.size):
            for c in range(self.size):
                if self.hidden_board[r][c] == "M":
                    if not self.flags[r][c]:
                        return False
                else:
                    if not self.revealed[r][c]:
                        return False
        return True


def main():
    game = Minesweeper()
    game.print_board()
    
    while True:
        move = input("Enter move (reveal/flag) row col (1-8): ").split()
        if len(move) != 3:
            print("Invalid input. Format: reveal/flag row col")
            continue
        action, r, c = move[0], int(move[1]) - 1, int(move[2]) - 1
        if not (0 <= r < 8 and 0 <= c < 8):
            print("Row/Col out of range.")
            continue

        if action == "reveal":
            game_over = game.reveal(r, c)
            if game_over:
                game.print_board()
                print("💀 You lost!")
                break
        elif action == "flag":
            game.flag(r, c)
        else:
            print("Unknown action. Use 'reveal' or 'flag'.")

        game.print_board()

        if game.check_win():
            print("🎉 You won! All mines cleared.")
            break


if __name__ == "__main__":
    main()
