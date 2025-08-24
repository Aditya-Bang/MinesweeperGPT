from dataclasses import dataclass
from typing import List

@dataclass
class MinesweeperExample:
    input: str
    board_state: List[List[str]]
    hidden_state: List[List[str]]
