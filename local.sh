#!/bin/bash

# ============================================================
# GrandFlow - LOCAL MODE - DRAFT
# Full stack in Docker for non-technical users
# Everything runs inside Docker (no local services needed)
# ============================================================

set -e

MODE="$1"
COMPOSE_FILE="docker-compose.local.yml"

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
        print_header "Starting LOCAL MODE"
        print_info "Building and starting all services (this may take a few minutes)..."
        DOCKER_BUILDKIT=1 docker compose -f "$COMPOSE_FILE" up -d --build
        print_success "All services started!"
        echo ""
        echo -e "${GREEN}LOCAL MODE is ready!${NC}"
        echo ""
        echo -e "${YELLOW}Available endpoints:${NC}"
        echo "  Frontend:       http://localhost:3000"
        echo "  Nginx Proxy:    http://localhost:8082"
        echo "  API Gateway:    http://localhost:8080"
        echo "  Users Service:  http://localhost:8000"
        echo "  Budget Service: http://localhost:8001"
        echo ""
        echo -e "${YELLOW}Database:${NC}"
        echo "  Host:     localhost:5432"
        echo "  User:     postgres"
        echo "  Password: postgres"
        echo "  Databases: grandflow_users, grandflow_budget"
        ;;

    down)
        print_header "Stopping LOCAL MODE"
        docker compose -f "$COMPOSE_FILE" down
        print_success "LOCAL MODE stopped"
        ;;

    logs)
        SERVICE="$2"
        if [ -z "$SERVICE" ]; then
            docker compose -f "$COMPOSE_FILE" logs -f
        else
            docker compose -f "$COMPOSE_FILE" logs -f "$SERVICE"
        fi
        ;;

    status)
        print_header "LOCAL MODE Status"
        docker compose -f "$COMPOSE_FILE" ps
        ;;

    rebuild)
        print_header "Rebuilding LOCAL MODE containers"
        DOCKER_BUILDKIT=1 docker compose -f "$COMPOSE_FILE" build --no-cache
        print_success "Containers rebuilt"
        ;;

    clean)
        print_header "Cleaning up LOCAL MODE"
        docker compose -f "$COMPOSE_FILE" down -v
        print_success "LOCAL MODE cleaned (volumes removed)"
        ;;

    shell)
        SERVICE="${2:-users}"
        print_info "Opening shell in $SERVICE container..."
        docker compose -f "$COMPOSE_FILE" exec "$SERVICE" /bin/bash
        ;;

    *)
        echo "Usage: ./local.sh {up|down|logs|status|rebuild|clean|shell}"
        echo ""
        echo "Commands:"
        echo "  up       - Start all services (full stack)"
        echo "  down     - Stop all services"
        echo "  logs [SERVICE] - View logs (optional: specify service)"
        echo "  status   - Show container status"
        echo "  rebuild  - Rebuild containers without cache"
        echo "  clean    - Stop and remove volumes"
        echo "  shell [SERVICE] - Open shell in a container (default: users)"
        exit 1
        ;;
esac
