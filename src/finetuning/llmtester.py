from src.models import Move
from src.globals import MAX_SEQUENCE_LENGTH as max_seq_length, MAX_PROMPT_LENGTH as max_prompt_length

from typing import List, Dict, Optional
import re
from pprint import pprint
from datasets import Dataset
from vllm import SamplingParams

class LLMTester:
    def __init__(self, model, tokenizer, dataset: Dataset, lora_request = None):
        self.model = model
        self.tokenizer = tokenizer
        self.dataset: Dataset = dataset
        self.lora_request = lora_request

    def test_llm(self, verbose: bool = False, print_every: int = 1):
        moves_correct = 0
        for idx, example in enumerate(self.dataset):
            prompt = example["prompt"]
            board_state: List[List[str]] = example["board_state"]
            hidden_state: List[List[str]] = example["hidden_state"]

            llm_move: str = self.generate_llm_move(prompt)
            if verbose and (idx % print_every == 0):
                print(f"Board state:")
                pprint(board_state)
                print(f"Hidden state:")
                pprint(hidden_state)
                print(f"LLM Move:\n{llm_move}")

            parsed_llm_move: Optional[Move] = self.parse_llm_move(llm_move)
            if not parsed_llm_move:
                if verbose and (idx % print_every == 0): print(f"Error parsing llm move: {llm_move}")
                continue

            if not self.validate_llm_move(parsed_llm_move, board_state):
                if verbose and (idx % print_every == 0): print(f"Invalid move: {parsed_llm_move}")
                continue

            if not self.verify_llm_move(parsed_llm_move, hidden_state):
                if verbose and (idx % print_every == 0): print(f"Move incorrect: {parsed_llm_move}")
                continue

            moves_correct += 1
            if verbose and (idx % print_every == 0): print(f"Move correct!")

        print(f"Moves correct: {moves_correct}/{len(self.dataset)}")
        print(f"Moves incorrect: {len(self.dataset) - moves_correct}/{len(self.dataset)}")

    def generate_llm_move(self, prompt: List[Dict[str, str]]) -> str:
        text = self.tokenizer.apply_chat_template(
            prompt,
            tokenize=False,
            add_generation_prompt=True,
        )
        sampling_params = SamplingParams(
            temperature=0.0,
            top_k=-1,
            top_p=1.0,
            max_tokens=max_seq_length-max_prompt_length,
        )
        output: str = self.model.fast_generate(
            text,
            sampling_params=sampling_params,
            lora_request=self.lora_request,
        )[0].outputs[0].text
        return output

    def parse_llm_move(self, llm_move: str) -> Optional[Move]:
        pattern = r"row:\s*(\d+),\s*col:\s*(\d+),\s*action:\s*(reveal|flag)"
        match = re.search(pattern, llm_move.strip(), re.DOTALL)
        if match:
            row, col, action = match.groups()
            return Move(row=int(row)-1, col=int(col)-1, action=action)  # 0-indexed
        return None

    def validate_llm_move(self, move: Move, board_state: List[List[str]]) -> bool:
        rows = len(board_state)
        cols = len(board_state[0])
        if not (0 <= move.row < rows and 0 <= move.col < cols):
            return False  # Out of bounds
        if board_state[move.row][move.col] != "*":  # Already revealed or flagged
            return False
        return True

    def verify_llm_move(self, move: Move, hidden_state: List[List[str]]) -> bool:
        cell_value = hidden_state[move.row][move.col]
        if move.action == "reveal":
            return cell_value != "M"  # Should not reveal a mine
        elif move.action == "flag":
            return cell_value == "M"  # Should only flag mines
        return False
