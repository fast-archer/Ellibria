#!/usr/bin/env bash
set -e

echo "🔧 Installing system dependencies..."

# Сначала обновим систему (критично для Arch!)
echo "📦 Updating system packages..."
sudo pacman -Syu --noconfirm

# Устанавливаем webkit2gtk с флагом --needed (не переустанавливать если есть)
echo "🌐 Installing webkit2gtk..."
sudo pacman -S --needed --noconfirm webkit2gtk-4.1 python-pywebview

# Остальные зависимости
sudo pacman -S --needed --noconfirm python python-pip tk

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
