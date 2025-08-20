# src/utils.py
from pathlib import Path

def get_base_directory() -> Path:
    """
    Returns the base directory path of the project.
    """
    return Path(__file__).resolve().parent.parent
