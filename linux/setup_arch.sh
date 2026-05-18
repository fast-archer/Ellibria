#!/usr/bin/env bash
set -e
echo "🔧 Installing system dependencies..."
sudo pacman -Sy --noconfirm python python-pip tk webkit2gtk python-pywebview
echo "🌐 Creating virtual environment..."
python -m venv venv
source venv/bin/activate
echo "⚙️ Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Done! Run with: ./run_arch.sh"