#!/bin/bash
# isolation_test.sh - Member 4 (IT24101240)
# Verifies Stage 5 container cannot reach CTFd, DB, or internet.

echo "========================================="
echo "  Stage 5 Isolation Tests"
echo "========================================="

test_reach() {
    local target="$1"
    local port="$2"
    local label="$3"
    docker exec stage5-linux bash -c "timeout 2 bash -c '</dev/tcp/$target/$port'" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "  [✗] $label - REACHABLE (isolation BROKEN)"
    else
        echo "  [✓] $label - BLOCKED (isolation OK)"
    fi
}

test_reach "ctf-playbox-ctfd-1" "8000" "CTFd container (port 8000)"
test_reach "ctf-playbox-db-1"   "3306" "DB container (port 3306)"
test_reach "8.8.8.8"            "53"   "Internet (8.8.8.8:53)"

echo "========================================="
echo "  Tests complete"
echo "========================================="