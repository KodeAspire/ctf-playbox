#!/bin/bash
docker-compose down -v
docker-compose up -d --build
echo "Stage 5 reset done."