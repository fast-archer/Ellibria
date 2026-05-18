cd ~/echoai/linux && cat > run_arch.sh << 'EOF'
#!/usr/bin/env bash
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"

if [ ! -d "$SCRIPT_DIR/venv" ]; then
    echo "❌ Virtual environment not found. Run: sudo ./setup_arch.sh"
    exit 1
fi

source "$SCRIPT_DIR/venv/bin/activate"
echo "🚀 Launching Echo..."
cd "$REPO_DIR" || exit
python setup_and_run.py
EOF
chmod +x run_arch.sh
