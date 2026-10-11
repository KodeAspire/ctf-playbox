#!/bin/bash
# Reset only the stage 5 challenge container

cd "$(dirname "$0")"

echo "[*] Recreating stage5-linux container..."
docker compose up -d --force-recreate --build stage5-linux

echo "[+] Stage 5 reset complete."
