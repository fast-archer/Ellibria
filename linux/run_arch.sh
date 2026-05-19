#!/usr/bin/env bash
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"

if [ ! -d "$SCRIPT_DIR/venv" ]; then
    echo "❌ Virtual environment not found. Run: sudo ./setup_arch.sh"
    exit 1
fi

source "$SCRIPT_DIR/venv/bin/activate"
cd "$REPO_DIR" || exit

echo "🚀 Starting Echo..."
echo "   Browser will open automatically at http://127.0.0.1:5000"
echo "   Press Ctrl+C to stop."
echo ""

python setup_and_run_linux.py
