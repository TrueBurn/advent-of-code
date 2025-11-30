#!/bin/bash
# Code Quality Check Script for Advent of Code Solutions
# Run this before committing code

set -e

echo "🔍 Running code quality checks..."
echo ""

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: Must be run from repository root"
    exit 1
fi

# Get the directory to check (defaults to current directory)
TARGET_DIR="${1:-.}"

echo "📁 Checking directory: $TARGET_DIR"
echo ""

# Run Black formatter check
echo "🎨 Running Black formatter check..."
python3 -m black --line-length 100 --check "$TARGET_DIR"
echo "✅ Black check passed"
echo ""

# Run Flake8 linter
echo "🔎 Running Flake8 linter..."
python3 -m flake8 --max-line-length=100 --extend-ignore=E203,W503 "$TARGET_DIR"
echo "✅ Flake8 check passed"
echo ""

# Run isort import checker
echo "📦 Running isort import checker..."
python3 -m isort --check-only --profile black --line-length 100 "$TARGET_DIR"
echo "✅ isort check passed"
echo ""

echo "✨ All code quality checks passed!"
