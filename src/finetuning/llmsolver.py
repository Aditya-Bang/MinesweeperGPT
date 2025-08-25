# src/finetuning/llmsolver.py
from src.minesweeper.validboard import ValidBoard
from src.models import Move
from src.finetuning.prompt import format_example


class LLMSolver:
    def __init__(self, board: ValidBoard, model, tokenizer):
        self.board: ValidBoard = board
        self.model = model
        self.tokenizer = tokenizer

    def solve(self, problem: str) -> str:
        # Implement the logic to solve the problem using the LLM
        return f"Solved {problem} using {self.model_name}"

    def get_llm_move(self) -> str:
        # Implement the logic to get a single move from the LLM
        messages: dict = format_example(self.board.get_board_string())
        return f"Get single move using {self.model_name}"
    
    def parse_llm_move(self, llm_move: str) -> Move:
        # Implement the logic to parse the LLM move
        return Move(row=0, col=0, action="reveal")

    def make_move(self, move: Move):
        # Implement the logic to make a move on the board
        pass