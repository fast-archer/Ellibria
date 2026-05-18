#!/usr/bin/env bash
set -e

if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: sudo ./setup_arch.sh first"
    exit 1
fi

source venv/bin/activate
echo "🚀 Launching Echo..."
# Путь на уровень выше (../) потому что setup_and_run.py в корне репозитория
python ../setup_and_run.py
