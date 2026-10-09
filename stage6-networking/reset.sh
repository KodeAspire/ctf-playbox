#!/usr/bin/env bash
set -euo pipefail

STAGE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GENERATOR="$STAGE_DIR/solver/create_capture.py"
CAPTURE="$STAGE_DIR/challenge/rabbit_traffic.pcap"

echo "[*] Resetting Stage 6: The Final Trace"

if [[ ! -f "$GENERATOR" ]]; then
    echo "[!] Generator not found: $GENERATOR"
    exit 1
fi

python3 "$GENERATOR"

if [[ ! -s "$CAPTURE" ]]; then
    echo "[!] Capture file missing or empty."
    exit 1
fi

echo "[+] Stage 6 reset completed."
