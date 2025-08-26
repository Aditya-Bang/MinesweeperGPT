# src/finetuning/llmsolver.py
from src.minesweeper.validboard import ValidBoard
from src.models import Move
from src.finetuning.prompt import format_example
from typing import List, Dict


class LLMSolver:
    def __init__(self, board: ValidBoard, model, tokenizer):
        self.board: ValidBoard = board
        self.model = model
        self.tokenizer = tokenizer

    def solve(self, problem: str) -> str:
        # Implement the logic to solve the problem using the LLM
        # specifically get's an llm move, makes it, and checks if game over on valid board
        return f"Solved {problem} using {self.model_name}"
    
    def get_llm_move(self) -> Move:
        # generates, parses, and then validates llm move, i.e. it should be playable.
        pass

    def _generate_llm_move(self) -> str:
        prompt: List[Dict[str, str]] = format_example(self.board.get_board_string())
        text = self.tokenizer.apply_chat_template(
            prompt,
            tokenize=False,
            add_generation_prompt=True,
        )
        input_tokens = self.tokenizer([text], return_tensors="pt").to(self.model.device)
        generated_ids = self.model.generate(
            **input_tokens,
            max_new_tokens=512,
        )
        output_ids = generated_ids[0][len(input_tokens.input_ids[0]):].tolist()
        decoded_output: str = self.tokenizer.decode(output_ids, skip_special_tokens=True).strip("\n")
        return decoded_output
    
    def _parse_llm_move(self, llm_move: str) -> Move:
        # Implement the logic to parse the LLM move
        return Move(row=0, col=0, action="reveal")

    def _validate_llm_move(self, move: Move):
        # Implement the logic to validate the LLM move
        pass

    def make_llm_move(self):
        # updates valid board with llm move by playing it.
        pass