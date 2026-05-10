#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"
VENV_DIR="${VENV_DIR:-.venv}"

cd "$ROOT"

"$PYTHON_BIN" -m venv "$VENV_DIR"

if [[ "${ARE2TRAIN_INSTALL_EDITABLE:-0}" == "1" ]]; then
  "$VENV_DIR/bin/python" -m pip install --no-build-isolation -e .
else
  echo "Skip editable install. Set ARE2TRAIN_INSTALL_EDITABLE=1 if you need it."
fi

"$VENV_DIR/bin/python" scripts/doctor.py

echo
echo "ARE2Train environment is ready."
echo "Activate it with: source $VENV_DIR/bin/activate"
