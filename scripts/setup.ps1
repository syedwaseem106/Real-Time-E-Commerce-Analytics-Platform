# ==============================================================================
# POWERSHELL SETUP SCRIPT FOR WINDOWS
# ==============================================================================

Write-Host "======================================================" -ForegroundColor Blue
Write-Host "🚀 Initiating E-Commerce Analytics Platform Windows Setup" -ForegroundColor Blue
Write-Host "======================================================" -ForegroundColor Blue

# 1. Verify Docker is running
try {
    $dockerCheck = docker compose version
    Write-Host "Docker is installed and running." -ForegroundColor Green
} catch {
    Write-Host "Error: Docker or Docker Compose is not installed or running. Please start Docker Desktop." -ForegroundColor Red
    Exit 1
}

# 2. Create host directories
Write-Host "Creating host-level directories..." -ForegroundColor Green
New-Item -ItemType Directory -Force -Path "logs", "data/exports", "data/sample", "docs/screenshots" | Out-Null

# 3. Spin up docker compose
Write-Host "Building and launching docker containers (in detached mode)..." -ForegroundColor Green
docker compose up -d --build

# 4. Wait for PostgreSQL Warehouse container to be healthy
Write-Host "Waiting for PostgreSQL Warehouse container to be healthy..." -ForegroundColor Yellow
$retries = 30
$healthy = $false
while ($retries -gt 0 -and -not $healthy) {
    $status = docker inspect --format='{{json .State.Health.Status}}' postgres 2>$null
    if ($status -eq '"healthy"') {
        $healthy = $true
    } else {
        Start-Sleep -Seconds 2
        $retries--
    }
}

if (-not $healthy) {
    Write-Host "Warning: Postgres didn't transition to healthy in time. Attempting seeding anyway..." -ForegroundColor Yellow
} else {
    Write-Host "PostgreSQL is healthy and reachable!" -ForegroundColor Green
}

Start-Sleep -Seconds 5

# 5. Seed relational dimensions
Write-Host "Seeding relational dimensions (Users, Products, Time)..." -ForegroundColor Green
docker compose exec -T spark-master python /app/src/warehouse/seed_dimensions.py

Write-Host "======================================================" -ForegroundColor Blue
Write-Host "🎉 Platform successfully deployed and seeded!" -ForegroundColor Green
Write-Host "======================================================" -ForegroundColor Blue
Write-Host "Access URLs:" -ForegroundColor Yellow
Write-Host "- Spark Master UI:    http://localhost:8080" -ForegroundColor White
Write-Host "- Airflow Web UI:     http://localhost:8081 (admin / admin)" -ForegroundColor White
Write-Host "- MinIO Storage UI:   http://localhost:9001 (minioadmin / minioadmin123)" -ForegroundColor White
Write-Host "======================================================" -ForegroundColor Blue
