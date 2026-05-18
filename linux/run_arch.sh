#!/usr/bin/env bash
set -e

if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: sudo ./setup_arch.sh first"
    exit 1
fi

source venv/bin/activate
echo "🚀 Launching Echo..."
python setup_and_run.py
