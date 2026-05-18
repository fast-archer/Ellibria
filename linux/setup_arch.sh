#!/usr/bin/env bash
set -e

echo "🔧 Installing system dependencies..."
# Для CachyOS/Arch: используем актуальный webkit2gtk
sudo pacman -Sy --noconfirm python python-pip tk webkit2gtk-4.1 python-pywebview

echo "🌐 Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  venv already exists, removing..."
    rm -rf venv
fi
python -m venv venv

echo "⚙️ Installing Python packages..."
source venv/bin/activate
pip install --upgrade pip
if [ -f "../requirements.txt" ]; then
    pip install -r ../requirements.txt
else
    pip install flask pywebview requests openai google-generativeai
fi

echo "✅ Done! Run with: ./run_arch.sh"
