#!/usr/bin/env bash
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"

if [ ! -d "$SCRIPT_DIR/venv" ]; then
    echo "❌ Venv not found. Run: sudo ./setup_arch.sh first"
    exit 1
fi

source "$SCRIPT_DIR/venv/bin/activate"
echo "🚀 Launching Echo..."
cd "$REPO_DIR" || exit
python setup_and_run.py
