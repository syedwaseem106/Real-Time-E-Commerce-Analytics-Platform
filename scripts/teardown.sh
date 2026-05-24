#!/usr/bin/env bash
# ==============================================================================
# E-COMMERCE ANALYTICS PLATFORM - TEARDOWN SCRIPT
# ==============================================================================

set -eo pipefail

YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}======================================================${NC}"
echo -e "${YELLOW}⚠️ Stopping and purging platform containers${NC}"
echo -e "${YELLOW}======================================================${NC}"

# Spin down compose stack, purging anonymous volumes to reset database baselines
docker compose down -v

echo -e "${YELLOW}Cleaning logs directory...${NC}"
rm -rf logs/*

echo -e "${RED}Platform shut down. All volumes purged successfully.${NC}"
