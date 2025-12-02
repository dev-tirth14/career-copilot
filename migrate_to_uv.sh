#!/bin/bash
# Migration script from pip to UV

set -e  # Exit on error

echo "================================"
echo "Migrating to UV"
echo "================================"
echo ""

# Check if UV is installed
if ! command -v uv &> /dev/null; then
    echo "❌ UV is not installed!"
    echo ""
    echo "Install UV with one of these methods:"
    echo "  • curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo "  • brew install uv"
    echo "  • pip install uv"
    echo ""
    exit 1
fi

echo "✓ UV is installed: $(uv --version)"
echo ""

# Backup old venv if it exists
if [ -d "venv" ]; then
    echo "📦 Backing up old venv..."
    mv venv venv.backup
    echo "✓ Old venv backed up to venv.backup/"
    echo ""
fi

# Remove .venv if it exists
if [ -d ".venv" ]; then
    echo "🗑️  Removing old .venv..."
    rm -rf .venv
    echo ""
fi

# Create new venv with UV
echo "🔧 Creating new virtual environment with UV..."
uv venv
echo "✓ Virtual environment created at .venv/"
echo ""

# Activate venv
echo "🔌 Activating virtual environment..."
source .venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Install dependencies
echo "📥 Installing dependencies from pyproject.toml..."
echo "   (This will be MUCH faster than pip!)"
uv sync
echo "✓ Dependencies installed"
echo ""

# Optional: Install dev dependencies
read -p "Install dev dependencies (pytest, black, ruff, mypy)? [y/N] " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📥 Installing dev dependencies..."
    uv sync --group dev
    echo "✓ Dev dependencies installed"
    echo ""
fi

# Generate uv.lock if it doesn't exist
if [ ! -f "uv.lock" ]; then
    echo "🔒 Generating lock file..."
    uv lock
    echo "✓ Lock file created"
    echo ""
fi

# Success message
echo "================================"
echo "✅ Migration Complete!"
echo "================================"
echo ""
echo "Next steps:"
echo "  1. Activate the new venv:"
echo "     source .venv/bin/activate"
echo ""
echo "  2. Test your application:"
echo "     python -m src.main"
echo ""
echo "  3. If everything works, remove backup:"
echo "     rm -rf venv.backup/"
echo ""
echo "UV Command Reference:"
echo "  • Add package:    uv add <package>"
echo "  • Remove package: uv remove <package>"
echo "  • Update all:     uv lock --upgrade && uv sync"
echo "  • Run script:     uv run python -m src.main"
echo ""
echo "See SETUP.md for more information!"
