# tests/finetuning/dataset.py
from src.finetuning.dataset import MinesweeperDataset
from src.models import MinesweeperExample
from src.finetuning.prompt import format_example
from typing import List


ds = MinesweeperDataset("data")
ex: MinesweeperExample = ds.load_examples()[0]
print(format_example(ex))
