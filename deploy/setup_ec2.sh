#!/bin/bash
set -euo pipefail

echo "=== RAG Application EC2 Setup ==="

# 1. System update
sudo apt update && sudo apt upgrade -y

# 2. Install Python 3.13 + dependencies
sudo apt install -y software-properties-common
sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt install -y python3.13 python3.13-venv python3.13-dev git curl

# 3. Install uv (fast Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"

# 4. Set up project directory
PROJECT_DIR="$HOME/MyProject"
if [ ! -d "$PROJECT_DIR" ]; then
    echo "ERROR: Project directory not found at $PROJECT_DIR"
    echo "Please copy/clone your project first:"
    echo "  scp -r -i your-key.pem ./MyProject ubuntu@<ip>:~/"
    exit 1
fi

cd "$PROJECT_DIR"

# 5. Create virtual environment and install dependencies
uv venv .venv --python python3.13
source .venv/bin/activate
uv pip install -e .

# 6. Verify .env exists
if [ ! -f .env ]; then
    echo "ERROR: .env file not found. Copy your .env with API keys:"
    echo "  scp -i your-key.pem .env ubuntu@<ip>:~/MyProject/"
    exit 1
fi

# 7. Create knowledge_base directory and copy PDFs
mkdir -p knowledge_base
if [ -z "$(ls -A knowledge_base/ 2>/dev/null)" ]; then
    echo "WARNING: knowledge_base/ is empty."
    echo "Copy your PDFs: scp -r -i key.pem ./AI-RAG-DOCS/* ubuntu@<ip>:~/MyProject/knowledge_base/"
fi

# 8. Run ingestion (if PDFs present)
if [ -n "$(ls -A knowledge_base/*.pdf 2>/dev/null)" ]; then
    echo "Running ingestion..."
    python scripts/ingest.py --action full --path ./knowledge_base/
fi

# 9. Install systemd service
sudo cp deploy/rag-app.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable rag-app
sudo systemctl start rag-app

echo ""
echo "=== Setup Complete ==="
echo "Application running at http://$(curl -s ifconfig.me):8501"
echo "Check status: sudo systemctl status rag-app"
echo "View logs:    sudo journalctl -u rag-app -f"
