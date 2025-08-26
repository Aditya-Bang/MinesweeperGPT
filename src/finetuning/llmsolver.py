# src/finetuning/llmsolver.py
import re
from src.minesweeper.validboard import ValidBoard
from src.models import Move
from src.finetuning.prompt import format_example
from typing import List, Dict, Optional


class LLMSolver:
    def __init__(self, valid_board: ValidBoard, model, tokenizer):
        self.valid_board: ValidBoard = valid_board
        self.model = model
        self.tokenizer = tokenizer

    def solve(self, verbose: bool) -> bool:
        # Implement the logic to solve the problem using the LLM
        # specifically get's an llm move, makes it, and checks if game over on valid board
        if verbose: print("LLM solving the following board:")
        if verbose: self.valid_board.print_board()

        while True:
            try:
                llm_move: str = self._generate_llm_move()
                move: Move = self._parse_llm_move(llm_move)
                if self._validate_llm_move(move):
                    self.make_llm_move(move)
                    if self.valid_board.is_game_over():
                        self.game_over = True
                else:
                    if verbose: print(f"Invalid move: {llm_move}")
            except:
                print("LLM failed to solve board.")
                return False

    def _generate_llm_move(self) -> str:
        prompt: List[Dict[str, str]] = format_example(self.valid_board.get_board_string())
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
        pattern = r"row:\s*(\d+),\s*col:\s*(\d+),\s*action:\s*(reveal|flag)"
        match = re.search(pattern, llm_move.strip(), re.DOTALL)
        if not match:
            raise ValueError(f"Cannot parse LLM output: {llm_move}")
        row, col, action = match.groups()
        return Move(row=row-1, col=col-1, action=action)  # Convert to 0-indexed

    def _validate_llm_move(self, move: Move):
        # Implement the logic to validate the LLM move, whether within the bounds of the board, and square is not already revealed or flagged
        if not (0 <= move.row < self.valid_board.rows and 0 <= move.col < self.valid_board.cols):
            return False
        if self.valid_board.is_revealed(move.row, move.col) or self.valid_board.is_flagged(move.row, move.col):
            return False
        return True

    def make_llm_move(self, move: Move):
        # updates valid board with llm move by playing it.
        if move.action == "reveal":
            self.valid_board.reveal(move.row, move.col)
        elif move.action == "flag":
            self.valid_board.flag(move.row, move.col)
