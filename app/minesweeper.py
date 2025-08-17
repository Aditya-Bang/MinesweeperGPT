import random

class Minesweeper:
    def __init__(self, size=8, min_mines=10, max_mines=13):
        self.size = size
        self.min_mines = min_mines
        self.max_mines = max_mines
        self.num_mines = 0
        self.hidden_board = [[0 for _ in range(size)] for _ in range(size)]
        self.board = [['*' for _ in range(size)] for _ in range(size)]
        self.revealed = [[False for _ in range(size)] for _ in range(size)]
        self.flags = [[False for _ in range(size)] for _ in range(size)]
        self.first_move = True

    def _place_mines(self, safe_r, safe_c):
        """Place mines ensuring safe_r, safe_c is not a mine and is a 0."""
        while True:
            # reset board
            self.hidden_board = [[0 for _ in range(self.size)] for _ in range(self.size)]
            self.num_mines = random.randint(self.min_mines, self.max_mines)
            mines = 0
            forbidden = {(safe_r, safe_c)}
            
            # place mines
            while mines < self.num_mines:
                r, c = random.randint(0, self.size-1), random.randint(0, self.size-1)
                if (r, c) not in forbidden and self.hidden_board[r][c] != "M":
                    self.hidden_board[r][c] = "M"
                    mines += 1
            
            self._compute_numbers()
            
            # ensure first cell is a 0
            if self.hidden_board[safe_r][safe_c] == 0:
                break

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
                    nr, nc = r+dr, c+dc
                    if 0 <= nr < self.size and 0 <= nc < self.size and self.hidden_board[nr][nc] == "M":
                        count += 1
                self.hidden_board[r][c] = count

    def reveal(self, r, c):
        if self.first_move:
            self._place_mines(r, c)
            self.first_move = False
        
        if self.flags[r][c] or self.revealed[r][c]:
            return False
        
        self.revealed[r][c] = True
        val = self.hidden_board[r][c]
        if val == "M":
            self.board[r][c] = "X"
            return True
        self.board[r][c] = str(val)
        
        if val == 0:
            for dr in [-1,0,1]:
                for dc in [-1,0,1]:
                    nr, nc = r+dr, c+dc
                    if 0 <= nr < self.size and 0 <= nc < self.size and not self.revealed[nr][nc]:
                        self.reveal(nr, nc)
        return False
