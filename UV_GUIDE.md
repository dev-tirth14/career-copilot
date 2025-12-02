# UV Quick Reference Guide

UV is a fast Python package manager that replaces pip and virtualenv. It's 10-100x faster than pip!

## Initial Setup

### Install UV
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with Homebrew
brew install uv

# Or with pip
pip install uv
```

### Migrate from pip
```bash
# Run the included migration script
bash migrate_to_uv.sh
```

This will:
- Create a `.venv` virtual environment
- Install all dependencies from `pyproject.toml`
- Generate a `uv.lock` file for reproducible builds

## Daily Usage

### Activate Virtual Environment
```bash
source .venv/bin/activate
```

### Install Dependencies
```bash
# Install all dependencies
uv sync

# Install with dev dependencies
uv sync --group dev

# Install after adding new dependencies
uv sync
```

### Add/Remove Packages
```bash
# Add a package
uv add requests

# Add a dev dependency
uv add --group dev pytest

# Remove a package
uv remove requests

# Update a specific package
uv add --upgrade requests

# Update all packages
uv lock --upgrade && uv sync
```

### Run Python Scripts
```bash
# Run with activated venv
python -m src.main

# Or run directly with UV (auto-activates venv)
uv run python -m src.main

# Run any command in the venv
uv run pytest
uv run black .
uv run mypy src/
```

## Project Structure

- `pyproject.toml` - Package metadata and dependencies
- `uv.lock` - Locked dependency versions (commit this!)
- `.venv/` - Virtual environment (don't commit)

## Common Commands

| Task | Command |
|------|---------|
| Create venv | `uv venv` |
| Install deps | `uv sync` |
| Add package | `uv add <package>` |
| Remove package | `uv remove <package>` |
| Update all | `uv lock --upgrade && uv sync` |
| Run script | `uv run python script.py` |
| Install from lock | `uv sync --frozen` |

## Benefits Over pip

- **10-100x faster** installation
- **Unified tool** (replaces pip, pip-tools, virtualenv)
- **Better resolution** of dependency conflicts
- **Reproducible builds** with lock files
- **Zero config** - works with existing `pyproject.toml`

## Troubleshooting

### Lock file out of sync
```bash
uv lock
uv sync
```

### Clean install
```bash
rm -rf .venv uv.lock
uv venv
uv sync
```

### Check what's installed
```bash
uv pip list
```

### See dependency tree
```bash
uv pip tree
```

## Migration from requirements.txt

UV automatically reads `pyproject.toml`. After migration:

1. Verify everything works: `uv sync && python -m src.main`
2. Delete `requirements.txt` (no longer needed)
3. Commit `uv.lock` to git

## CI/CD Integration

```yaml
# GitHub Actions example
- name: Install UV
  run: curl -LsSf https://astral.sh/uv/install.sh | sh

- name: Install dependencies
  run: uv sync --frozen

- name: Run tests
  run: uv run pytest
```

## Learn More

- [UV Documentation](https://docs.astral.sh/uv/)
- [UV GitHub](https://github.com/astral-sh/uv)
