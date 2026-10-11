#!/bin/bash

# Confirms the CTF Play Box is correctly deployed and isolated.

set -u

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_DIR"

echo " CTF Play Box - Deployment Verification"
echo ""

echo "[1] Container status:"
docker compose ps
echo ""

echo "[2] CTFd reachability:"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000 2>/dev/null || echo "000")
if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "302" ]; then
    echo "    [OK] CTFd is responding (HTTP $HTTP_CODE)"
else
    echo "    [FAIL] CTFd returned HTTP $HTTP_CODE"
fi
echo ""

echo "[3] Stage 5 SSH port (2222):"
if nc -z localhost 2222 2>/dev/null; then
    echo "    [OK] Port 2222 is open"
else
    echo "    [FAIL] Port 2222 is not reachable"
fi
echo ""

echo "[4] Stage 3 intranet port (8080):"
if nc -z localhost 8080 2>/dev/null; then
    echo "    [OK] Port 8080 is open"
else
    echo "    [WARN] Port 8080 is not reachable (if Stage 3 uses it)"
fi
echo ""

echo "[5] Database seed check:"
USER_COUNT=$(docker compose exec -T ctfd python -c \
    "from CTFd.models import Users; print(Users.query.count())" 2>/dev/null || echo "0")
if [ "$USER_COUNT" -gt 0 ] 2>/dev/null; then
    echo "    [OK] Database has $USER_COUNT user(s)"
else
    echo "    [FAIL] Database appears empty"
fi
echo ""

echo "[6] Isolation test (Stage 5 cannot reach CTFd):"
if docker compose exec -T stage5-linux sh -c "getent hosts ctfd" >/dev/null 2>&1; then
    echo "    [FAIL] stage5-linux can resolve 'ctfd' - isolation broken"
else
    echo "    [OK] stage5-linux cannot resolve 'ctfd' - isolated"
fi
echo ""

echo "[7] UFW rules:"
sudo ufw status numbered 2>/dev/null | head -20 || echo "    (ufw status requires sudo)"
echo ""
echo " Verification complete."
