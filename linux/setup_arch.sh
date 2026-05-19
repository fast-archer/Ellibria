#!/usr/bin/env bash
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"

echo "🔧 Updating system..."
sudo pacman -Syu --noconfirm

echo "📦 Installing dependencies..."
sudo pacman -S --needed --noconfirm python python-pip tk xdg-utils

echo "🌐 Creating virtual environment..."
[ -d "$SCRIPT_DIR/venv" ] && rm -rf "$SCRIPT_DIR/venv"
python -m venv "$SCRIPT_DIR/venv"

echo "⚙️ Installing Python packages..."
source "$SCRIPT_DIR/venv/bin/activate"
pip install --upgrade pip
pip install flask openai requests

echo ""
echo "✅ Done! Run: ./run_arch.sh"
