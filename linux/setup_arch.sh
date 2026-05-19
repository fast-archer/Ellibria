#!/usr/bin/env bash
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "📦 Installing system dependencies via pacman..."
# sudo запрашивается только здесь и только для системных пакетов
sudo pacman -S --needed --noconfirm python tk xdg-utils

echo "🌐 Creating virtual environment (as current user)..."
if [ -d "$SCRIPT_DIR/venv" ]; then
    rm -rf "$SCRIPT_DIR/venv"
fi

# Создаем venv с правами текущего пользователя
python -m venv "$SCRIPT_DIR/venv"

echo "⚙️ Installing Python packages..."
source "$SCRIPT_DIR/venv/bin/activate"

# Обновляем pip и ставим пакеты локально внутри venv
pip install --upgrade pip
pip install flask openai requests

echo ""
echo "✅ Done! Now you can run: ./run_arch.sh"
