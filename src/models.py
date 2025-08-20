from dataclasses import dataclass
from typing import List

@dataclass
class MinesweeperExample:
    input: str
    action: str
    hidden_state: List[str]
