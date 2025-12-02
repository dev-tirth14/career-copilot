# Setup Guide - Career Copilot

This project uses **UV** for fast, modern Python dependency management.

## Prerequisites

- Python 3.10 or higher
- Ollama (for local LLM)

## Setup Steps

### 1. Install UV

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with Homebrew
brew install uv

# Or with pip
pip install uv
```

### 2. Clone and Setup Project

```bash
# Clone the repository
git clone <your-repo-url>
cd career-copilot

# Create virtual environment with UV
uv venv

# Activate the virtual environment
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate     # Windows

# Install all dependencies
uv sync

# Install with dev dependencies (for development)
uv sync --group dev
```

### 3. Install Ollama & Pull Model

```bash
# Install Ollama from https://ollama.ai
# Then pull the model
ollama pull llama3.2
```

### 4. Prepare Data Directories

The required directories are already created with `.gitkeep` files:
- `data/resumes/` - Place your resume PDFs here
- `data/knowledge/skills/` - Skill definition YAML files
- `data/vector_db/` - ChromaDB vector database (auto-created)
- `logs/` - Application logs

### 5. Process Knowledge Base (First Time Only)

```python
from src.core.knowledge.store import KnowledgeStore
from src.config.settings import Config

# Initialize and process knowledge
ks = KnowledgeStore(Config.KNOWLEDGE_PATH)
ks.process_knowledge()
```

### 6. Run the Application

```bash
# Make sure you're in the project root with venv activated
python -m src.main
```

## UV Command Reference

### Managing Dependencies

```bash
# Add a new package
uv add <package-name>

# Add a dev dependency
uv add --group dev <package-name>

# Remove a package
uv remove <package-name>

# Update all packages
uv lock --upgrade
uv sync

# Update a specific package
uv add --upgrade <package-name>
```

### Working with Virtual Environments

```bash
# Create venv
uv venv

# Create venv with specific Python version
uv venv --python 3.11

# Activate venv
source .venv/bin/activate

# Deactivate
deactivate
```

### Running Scripts

```bash
# Run Python with UV's venv automatically
uv run python -m src.main

# Run tests
uv run pytest

# Format code
uv run black src/

# Lint code
uv run ruff check src/

# Type check
uv run mypy src/
```

## Project Structure

```
career-copilot/
├── pyproject.toml          # Project config & dependencies (UV reads this!)
├── uv.lock                 # Lock file (auto-generated, like package-lock.json)
├── .venv/                  # Virtual environment
├── src/                    # Source code
│   ├── core/               # Business logic
│   ├── services/           # Application services
│   ├── models/             # Database models
│   └── ...
└── data/                   # Data files
```

## Development Workflow

### Adding a New Dependency

```bash
# Instead of pip install, use:
uv add langchain-openai

# This automatically:
# 1. Adds to pyproject.toml
# 2. Updates uv.lock
# 3. Installs the package
```

### Running Tests

```bash
# Install dev dependencies first
uv sync --group dev

# Run tests
uv run pytest

# With coverage
uv run pytest --cov=src --cov-report=html
```

### Code Quality

```bash
# Format code
uv run black src/

# Lint
uv run ruff check src/

# Type check
uv run mypy src/
```

## Migrating from requirements.txt

If you're migrating from an old setup:

```bash
# Remove old venv
rm -rf venv/

# Create new UV-managed venv
uv venv

# Install from pyproject.toml (already done!)
uv sync

# You can keep requirements.txt for backwards compatibility:
uv pip compile pyproject.toml -o requirements.txt
```

## Troubleshooting

### UV not found after installation

```bash
# Add UV to PATH (if installed via script)
export PATH="$HOME/.cargo/bin:$PATH"

# Or restart your terminal
```

### Wrong Python version

```bash
# Specify Python version explicitly
uv venv --python 3.10
```

### Dependencies not installing

```bash
# Clear UV cache
uv cache clean

# Reinstall
uv sync --reinstall
```

### Import errors after setup

```bash
# Make sure venv is activated
source .venv/bin/activate

# Verify installation
uv pip list
```

## Benefits of UV

✅ **10-100x faster** than pip
✅ **Lock file** - reproducible builds
✅ **Better dependency resolution** - no conflicts
✅ **Modern standard** - uses pyproject.toml
✅ **All-in-one** - replaces pip, pip-tools, virtualenv
✅ **Cross-platform** - works everywhere

## Additional Resources

- [UV Documentation](https://docs.astral.sh/uv/)
- [pyproject.toml Guide](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)
- [Project README](README.md)
