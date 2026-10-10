#!/usr/bin/env bash
set -euo pipefail

STAGE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EVIDENCE_DIR="$STAGE_DIR/challenge/evidence"
GENERATOR="$STAGE_DIR/solver/create_evidence.py"

echo "[*] Resetting Stage 4: Forensics"

if [[ ! -f "$GENERATOR" ]]; then
    echo "[!] Generator not found: $GENERATOR"
    exit 1
fi

python3 "$GENERATOR"

echo "[+] Stage 4 reset completed."
