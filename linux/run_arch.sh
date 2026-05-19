#!/usr/bin/env bash
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"

if [ ! -d "$SCRIPT_DIR/venv" ]; then
    echo "❌ Virtual environment not found. Please run: ./setup_arch.sh"
    exit 1
fi

# Активируем окружение с правильными правами доступа
source "$SCRIPT_DIR/venv/bin/activate"
cd "$REPO_DIR" || exit

echo "🚀 Starting Echo..."
echo "   App will launch in a dedicated window."
echo "   Press Ctrl+C in terminal to stop."
echo ""

# Запускаем РЕАЛЬНЫЙ файл из корня репозитория БЕЗ sudo
python setup_and_run.py
