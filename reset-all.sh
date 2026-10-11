#!/bin/bash
# Full platform reset
# Wipes ALL data including (users, scores, submissions) and restores from seed.

cd "$(dirname "$0")"

echo "[*] Stopping containers and wiping volumes..."
docker compose down -v

echo "[*] Starting fresh from seed..."
docker compose up -d

echo "Full reset complete."
