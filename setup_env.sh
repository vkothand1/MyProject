#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

if [ -d ".venv" ]; then
  echo ".venv already exists. To recreate, remove .venv first."
else
  echo "Creating virtual environment .venv"
  python3 -m venv .venv
fi

echo "Activating .venv and installing packages"
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install uv
python -m pip freeze > requirements.txt
echo "Done. Activate with: source .venv/bin/activate"
