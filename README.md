# MinesweeperGPT

```bash
export PYTHONPATH=.
uv venv
source .venv/bin/activate # .venv\Scripts\activate on windows cmd
uv pip install pytest unsloth vllm --torch-backend=auto
python main.py
```

Tests:
```
pytest tests/validboard.py
```

Project Structure:

tests/
    finetuning/
        base.py
        improved.py -> have play one game function, and for many tests, track success rate
llm/ -> store pickled llms somehow here
data/
    board/ -> enum from 0 to n in .txt files
    hidden_board/
src/
    minesweeper/
    datagen/
    finetuning/
main.py -> give args for either playing minesweeper yourself, running one game of default llm, or improved llm

TODOS:
1. maybe make small streamlit for demoing llm finetuned
2. finetuning -> dataset query is a step, solution is hidden state to be used in reward funcs for grpo
3. make game pure virtual class (only has play method), and person game, llm game sub classes

