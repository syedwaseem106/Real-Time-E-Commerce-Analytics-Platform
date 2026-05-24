#!/usr/bin/env bash
# ==============================================================================
# E-COMMERCE ANALYTICS PLATFORM - SETUP SCRIPT
# ==============================================================================

set -eo pipefail

# Terminal Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}======================================================${NC}"
echo -e "${BLUE}🚀 Initiating E-Commerce Analytics Platform Local Setup${NC}"
echo -e "${BLUE}======================================================${NC}"

# 1. Assert Docker & Compose installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker is not installed. Please install Docker before proceeding.${NC}"
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo -e "${RED}Error: Docker Compose is not available. Please install Docker Compose.${NC}"
    exit 1
fi

# 2. Creating host folders for volume bindings to avoid permission glitches
echo -e "${GREEN}Creating host-level directories...${NC}"
mkdir -p logs data/exports data/sample docs/screenshots

# 3. Spin up docker containers
echo -e "${GREEN}Building and launching docker containers (in detached mode)...${NC}"
docker compose up -d --build

# 4. Wait for services to achieve healthy states
echo -e "${YELLOW}Waiting for PostgreSQL Warehouse container to be healthy...${NC}"
until docker exec postgres pg_isready -U postgres -d ecommerce_warehouse &>/dev/null; do
    sleep 2
done
echo -e "${GREEN}PostgreSQL is healthy and reachable!${NC}"

echo -e "${YELLOW}Waiting for MinIO S3 container to start up...${NC}"
sleep 5 # Grace time for minio server startup

# 5. Pre-seed dimensional tables in warehouse database
echo -e "${GREEN}Seeding relational dimensions (Users, Products, Time)...${NC}"
# Submit seed execution inside Spark Master container or local shell if packages exist
# We will use Spark Master shell to execute database migrations and pre-seeding
docker compose exec -T spark-master python /app/src/warehouse/seed_dimensions.py

echo -e "${BLUE}======================================================${NC}"
echo -e "${GREEN}🎉 Platform successfully deployed and seeded!${NC}"
echo -e "${BLUE}======================================================${NC}"
echo -e "${YELLOW}Access URLs:${NC}"
echo -e "- Spark Master UI:    http://localhost:8080"
echo -e "- Airflow Web UI:     http://localhost:8081 (admin / admin)"
echo -e "- MinIO Storage UI:   http://localhost:9001 (minioadmin / minioadmin123)"
echo -e "${BLUE}======================================================${NC}"
