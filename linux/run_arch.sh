#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Фикс для "замерзающих" кликов в WebKit2GTK на Arch/CachyOS
export WEBKIT_DISABLE_COMPOSITING_MODE=1

echo "Launching Echo..."
source "$SCRIPT_DIR/venv/bin/activate"
python "$SCRIPT_DIR/../setup_and_run.py" linux
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
