from pathlib import Path

# Manages paths and settings
class Config:
    PROJECT_ROOT_DIR=Path(__file__).parent.parent.parent
    DATA_DIR=PROJECT_ROOT_DIR.joinpath("data")
    PROMPT_DIR=PROJECT_ROOT_DIR.joinpath("src","prompts")