#!/bin/bash

# Stage 1: The Altered ID - Reset Script
# Restores the original challenge artifact and clears completion state

echo "=========================================="
echo "Stage 1: The Altered ID - Reset"
echo "=========================================="

cd "$(dirname "$0")"

if [ -f "challenge/original_id.jpg" ]; then
    cp challenge/original_id.jpg challenge/rabbit_id.jpg
    echo "[+] Restored: challenge/rabbit_id.jpg"
    echo "[+] File size: $(stat -c%s challenge/rabbit_id.jpg) bytes"
    echo "[+] Reset complete."
else
    echo "[!] Original file not found."
    echo "[!] Run solver/create_stego.py first."
    exit 1
fi

echo "=========================================="
echo "Next: Clear Stage 1 completion in CTFd admin panel"
echo "=========================================="