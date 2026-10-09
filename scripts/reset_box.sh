#!/bin/bash
echo "Resetting Operation Rabbit CTF Box..."
# This assumes you are using Docker Compose
docker compose down -v
docker compose up -d
echo "Reset complete. Waiting for services to start..."
sleep 10
echo "Done."