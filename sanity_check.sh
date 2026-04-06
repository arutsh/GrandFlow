#!/bin/bash
# Sanity check script for GrandFlow (Unix/Mac/Linux)
# Runs black, mypy, and flake8 on Python code

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVICES=("users" "budget")
FIX_MODE=false

# Parse arguments
for arg in "$@"; do
    if [ "$arg" = "--fix" ]; then
        FIX_MODE=true
    fi
done

if [ "$FIX_MODE" = true ]; then
    echo -e "${YELLOW}Running in FIX mode (Black will auto-format)${NC}"
fi

echo -e "${BLUE}══════════════════════════════════════${NC}"
echo -e "${BLUE}GrandFlow Sanity Check${NC}"
echo -e "${BLUE}══════════════════════════════════════${NC}\n"

BACKEND_PASSED=true

# Check backend
echo -e "${YELLOW}═══ BACKEND SANITY CHECK ═══${NC}\n"

for service in "${SERVICES[@]}"; do
    echo -e "${YELLOW}Checking $service service...${NC}"
    SERVICE_PATH="$PROJECT_ROOT/services/$service"
    
    export PYTHONPATH="$SERVICE_PATH:$SERVICE_PATH/../../shared"
    
    # Black
    echo -e "${BLUE}► Running black...${NC}"
    if [ "$FIX_MODE" = true ]; then
        if black "$SERVICE_PATH/app" 2>/dev/null; then
            echo -e "${GREEN}✓ Black passed${NC}"
        else
            BACKEND_PASSED=false
        fi
    else
        if black --check "$SERVICE_PATH/app" 2>/dev/null; then
            echo -e "${GREEN}✓ Black passed${NC}"
        else
            echo -e "${RED}✗ Black failed${NC}"
            echo -e "${YELLOW}  Hint: Run with --fix to auto-format${NC}"
            BACKEND_PASSED=false
        fi
    fi
    
    # Mypy
    echo -e "${BLUE}► Running mypy...${NC}"
    if mypy "$SERVICE_PATH/app" 2>/dev/null; then
        echo -e "${GREEN}✓ Mypy passed${NC}"
    else
        echo -e "${RED}✗ Mypy failed${NC}"
        BACKEND_PASSED=false
    fi
    
    # Flake8
    echo -e "${BLUE}► Running flake8...${NC}"
    if flake8 "$SERVICE_PATH/app" 2>/dev/null; then
        echo -e "${GREEN}✓ Flake8 passed${NC}"
    else
        echo -e "${RED}✗ Flake8 failed${NC}"
        BACKEND_PASSED=false
    fi
    
    echo ""
done

# Summary
echo -e "${BLUE}══════════════════════════════════════${NC}"
echo -e "${BLUE}SUMMARY${NC}"
echo -e "${BLUE}══════════════════════════════════════${NC}"

if [ "$BACKEND_PASSED" = true ]; then
    echo -e "${GREEN}✓ All checks passed! 🎉${NC}"
    exit 0
else
    echo -e "${RED}✗ Some checks failed. See above for details.${NC}"
    exit 1
fi
