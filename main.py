from app.minesweeper import Minesweeper
from app.minesweepersolver import MinesweeperSolver

def main():
    game = Minesweeper()
    solver = MinesweeperSolver(game)

    while True:
        move = input("Enter move (reveal/flag) row col (1-8): ").split()
        if len(move) != 3:
            print("Invalid input. Format: reveal/flag row col")
            continue
        action, r, c = move[0], int(move[1]) - 1, int(move[2]) - 1

        if action == "reveal":
            game_over = game.reveal(r, c)
            if game_over:
                print("💥 Mine hit! Game over.")
                break
            if not solver.is_solvable():
                print("⚠️ Board not solvable, regenerating...")
                game = Minesweeper()
                solver = MinesweeperSolver(game)

        elif action == "flag":
            game.flags[r][c] = not game.flags[r][c]
            game.board[r][c] = "F" if game.flags[r][c] else "*"
        else:
            print("Invalid action. Use reveal/flag.")

        # display board
        for row in game.board:
            print(" ".join(row))
        print()

if __name__ == "__main__":
    main()
