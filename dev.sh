dev#!/bin/bash

# ============================================================
# GrandFlow - DEV MODE
# Infrastructure only: PostgreSQL, Redis, API Gateway, Nginx
# Frontend and Backend services run on local machine
# ============================================================

set -e

MODE="$1"
COMPOSE_FILE="docker-compose.dev.yml"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}→ $1${NC}"
}

case "$MODE" in
    up)
        print_header "Starting DEV MODE"
        print_info "Starting infrastructure (DB, Redis, Nginx)..."
        systemctl stop postgresql redis 2>/dev/null || true
        DOCKER_BUILDKIT=1 docker compose -f "$COMPOSE_FILE" up -d --build
        print_success "Infrastructure started!"
        echo ""
        echo -e "${GREEN}DEV MODE is ready!${NC}"
        echo ""
        echo -e "${YELLOW}Next steps:${NC}"
        echo "1. Start Users Service locally (port 8000):"
        echo "   cd services/users && alembic upgrade head && python -m uvicorn main:app --reload --port 8000"
        echo ""
        echo "2. Start Budget Service locally (port 8001) - in another terminal:"
        echo "   cd services/budget && alembic upgrade head && python -m uvicorn main:app --reload --port 8001"
        echo ""
        echo "3. Start Frontend locally - in another terminal:"
        echo "   cd frontend-typescript && npm run dev"
        echo ""
        echo "Or run: ./dev.sh services (for detailed commands)"
        echo ""
        echo -e "${YELLOW}Available endpoints:${NC}"
        echo "  Database:           localhost:5432"
        echo "  Redis:              localhost:6379"
        echo "  RabbitMQ:           localhost:5672 (AMQP), localhost:15672 (UI)"
        echo "  Nginx Proxy:        localhost:8082"
        echo "  Users Service:      localhost:8000 (run locally) - http://localhost:8000/docs"
        echo "  Budget Service:     localhost:8001 (run locally) - http://localhost:8001/docs"
        echo "  Frontend:           localhost:3000 (run locally)"
        echo ""
        echo -e "${YELLOW}Monitoring & Observability:${NC}"
        echo "  Jaeger Tracing:     http://localhost:16686"
        echo "  Prometheus Metrics: http://localhost:9090"
        echo "  Grafana Dashboards: http://localhost:3002 (admin:admin)"
        echo "  Users Metrics:      http://localhost:8003/metrics"
        echo "  Budget Metrics:     http://localhost:8002/metrics"
        ;;

    down)
        print_header "Stopping DEV MODE"
        docker compose -f "$COMPOSE_FILE" down
        print_success "DEV MODE stopped"
        ;;

    logs)
        docker compose -f "$COMPOSE_FILE" logs -f
        ;;

    status)
        print_header "DEV MODE Status"
        docker compose -f "$COMPOSE_FILE" ps
        ;;

    rebuild)
        print_header "Rebuilding DEV MODE containers"
        DOCKER_BUILDKIT=1 docker compose -f "$COMPOSE_FILE" build --no-cache
        print_success "Containers rebuilt"
        ;;

    services)
        print_header "Running Services Locally - Commands"
        echo ""
        echo -e "${YELLOW}Open new terminals and run these commands:${NC}"
        echo ""
        echo -e "${BLUE}=== Terminal 1: Users Service (port 8000) ===${NC}"
        echo "cd services/users"
        echo "alembic upgrade head"
        echo "python -m uvicorn main:app --reload --port 8000"
        echo ""
        echo -e "${BLUE}=== Terminal 2: Budget Service (port 8001) ===${NC}"
        echo "cd services/budget"
        echo "alembic upgrade head"
        echo "python -m uvicorn main:app --reload --port 8001"
        echo ""
        echo -e "${BLUE}=== Terminal 3: Frontend ===${NC}"
        echo "cd frontend-typescript"
        echo "npm install  # first time only"
        echo "npm run dev"
        echo ""
        echo -e "${YELLOW}Endpoints:${NC}"
        echo "  Frontend:       http://localhost:3000"
        echo "  Users API:      http://localhost:8000/docs"
        echo "  Budget API:     http://localhost:8001/docs"
        echo "  Nginx Proxy:    http://localhost:8082"
        echo ""
        echo -e "${YELLOW}Monitoring (already running in Docker):${NC}"
        echo "  Jaeger:         http://localhost:16686 (traces)"
        echo "  Prometheus:     http://localhost:9090 (metrics)"
        echo "  Grafana:        http://localhost:3001 (dashboards, admin:admin)"
        echo ""
        echo -e "${YELLOW}Note: .env.*.dev files already have localhost configured${NC}"
        ;;

    clean)
        print_header "Cleaning up DEV MODE"
        docker compose -f "$COMPOSE_FILE" down -v
        print_success "DEV MODE cleaned (volumes removed)"
        ;;

    *)
        echo "Usage: ./dev.sh {up|down|logs|status|rebuild|services|clean}"
        echo ""
        echo "Commands:"
        echo "  up       - Start infrastructure for dev mode"
        echo "  down     - Stop infrastructure"
        echo "  logs     - View logs"
        echo "  status   - Show container status"
        echo "  rebuild  - Rebuild containers without cache"
        echo "  services - Show commands to run services locally"
        echo "  clean    - Stop and remove volumes"
        exit 1
        ;;
esac
