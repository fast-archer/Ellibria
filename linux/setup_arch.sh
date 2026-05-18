#!/usr/bin/env bash
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"

echo "🔧 Updating system & installing dependencies..."
sudo pacman -Syu --noconfirm
sudo pacman -S --needed --noconfirm python python-pip tk webkit2gtk-4.1 python-pywebview

echo "🌐 Creating virtual environment..."
[ -d "$SCRIPT_DIR/venv" ] && rm -rf "$SCRIPT_DIR/venv"
python -m venv "$SCRIPT_DIR/venv"

echo "⚙️ Installing Python packages..."
source "$SCRIPT_DIR/venv/bin/activate"
pip install --upgrade pip
[ -f "$REPO_DIR/requirements.txt" ] && pip install -r "$REPO_DIR/requirements.txt" || pip install flask pywebview requests openai google-generativeai flask-session pillow

echo "✅ Done! Run: ./run_arch.sh"
