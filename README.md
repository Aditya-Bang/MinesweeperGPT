# MinesweeperGPT

MinesweeperGPT is a research project focused on teaching the Qwen 4B large language model to play Minesweeper using GRPO (Generalized Reinforcement Policy Optimization) finetuning and QLoRA (Quantized Low-Rank Adapter) techniques. The project provides a modular pipeline for data generation, model training, and evaluation, enabling scalable experimentation with LLM-based solvers for the classic Minesweeper game.

## Features

- **LLM Minesweeper Solver:** Integrates Qwen 4B as the core model for learning Minesweeper strategies.
- **GRPO Finetuning:** Utilizes GRPO for reinforcement learning-based policy optimization.
- **QLoRA Integration:** Efficient parameter-efficient finetuning with QLoRA adapters.
- **Custom Data Generation:** Scripts for generating Minesweeper game data for training and testing.
- **Evaluation Tools:** Utilities for benchmarking model performance on unseen Minesweeper boards.

## Project Structure

```
src/
  datagen/         # Data generation scripts and visualization tools
  finetuning/      # GRPO, QLoRA, and dataset handling modules
  minesweeper/     # Game logic, board representation, and solver interface
  globals.py       # Global configuration and constants
  models.py        # Model loading and management
  utils.py         # Utility functions
main.py            # Entry point for running experiments
README.md          # Project documentation
```

## Getting Started

1. **Install Dependencies**

Requires CUDA 12.4+ and Linux for the vLLM backend and finetuning, with at least 15 GB VRAM.

    ```bash
    export PYTHONPATH=.
    uv venv
    source .venv/bin/activate # .venv\Scripts\activate on windows cmd
    uv pip install -qqq torch==2.6.0 torchvision==0.21.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cu124
    uv pip install -qqq unsloth==2025.6.2 unsloth_zoo==2025.6.1 trl==0.18.1 vllm==0.8.5.post1 xformers==0.0.29.post2 triton==3.2.0 accelerate==1.7.0 transformers==4.51.3 torchao==0.12.0 wandb pytest
    ```

2. **Prepare Data**
    - Use scripts in `src/datagen/` to generate or preprocess Minesweeper game data.

3. **Finetune Qwen 4B**
    - Run GRPO finetuning with QLoRA adapters using notebooks in `src/finetuning/`.

4. **Evaluate the Model**
    - Use evaluation scripts to test the trained model on new Minesweeper boards.

## Key Files

- `src/finetuning/llmsolver.py`: LLM-based Minesweeper solver logic.
- `src/finetuning/MinesweeperGPT.ipynb`: Main script for GRPO finetuning with QLoRA.
- `src/datagen/datagen.py`: Data generation for Minesweeper games.

## Citation

If you use this project in your research, please cite or acknowledge the repository.

## License

This project is licensed under the MIT License.

---

For questions or contributions, please open an issue or pull request.
