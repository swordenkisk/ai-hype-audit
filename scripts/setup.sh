#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -e .

printf '\nSetup complete.\n'
printf 'Activate the environment with: source .venv/bin/activate\n'
printf 'Run tests with: .venv/bin/python -m unittest discover -s tests\n'
