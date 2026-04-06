#!/usr/bin/env python3
"""
Sanity check script for GrandFlow backend and frontend
Runs black, mypy, and flake8 on Python code
Runs npm linting on frontend

Usage:
    python sanity_check.py              # Check only
    python sanity_check.py --fix        # Fix black issues
    python sanity_check.py --backend    # Check backend only
    python sanity_check.py --frontend   # Check frontend only
"""

import os
import sys
import subprocess
from pathlib import Path

# Colors for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

project_root = Path(__file__).parent
services = ["users", "budget"]
fix_mode = "--fix" in sys.argv
should_check_backend = "--frontend" not in sys.argv
should_check_frontend = "--backend" not in sys.argv


def check_backend():
    """Check backend services with black, mypy, and flake8"""
    print(f"\n{YELLOW}═══ BACKEND SANITY CHECK ═══{RESET}")

    overall_success = True

    for service in services:
        service_path = project_root / "services" / service
        print(f"\n{YELLOW}Checking {service} service...{RESET}")

        # Set PYTHONPATH
        env = os.environ.copy()
        pythonpath = f"{service_path}:{service_path}/../../shared"
        env["PYTHONPATH"] = pythonpath

        # Black
        black_cmd = [sys.executable, "-m", "black", "--check", "./app"]
        if fix_mode:
            black_cmd = [sys.executable, "-m", "black", "./app"]

        result = subprocess.run(black_cmd, cwd=service_path, env=env, capture_output=False)
        if result.returncode != 0:
            overall_success = False
            if not fix_mode:
                print(f"{YELLOW}  Hint: Run with --fix to auto-format{RESET}")
        else:
            print(f"{GREEN}  ✓ Black passed{RESET}")

        # Mypy
        result = subprocess.run(
            [sys.executable, "-m", "mypy", "./app"],
            cwd=service_path,
            env=env,
            capture_output=False,
        )
        if result.returncode != 0:
            overall_success = False
        else:
            print(f"{GREEN}  ✓ Mypy passed{RESET}")

        # Flake8
        result = subprocess.run(
            [sys.executable, "-m", "flake8", "./app"],
            cwd=service_path,
            env=env,
            capture_output=False,
        )
        if result.returncode != 0:
            overall_success = False
        else:
            print(f"{GREEN}  ✓ Flake8 passed{RESET}")

    return overall_success


def check_frontend():
    """Check frontend with ESLint and TypeScript"""
    print(f"\n{YELLOW}═══ FRONTEND SANITY CHECK ═══{RESET}")

    frontend_path = project_root / "frontend-typescript"

    # Check if npm is available
    try:
        subprocess.run(
            ["npm", "--version"],
            capture_output=True,
            check=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        print(f"{YELLOW}⚠ npm not found. Skipping frontend checks.{RESET}")
        print(f"{YELLOW}Install Node.js to enable frontend linting.{RESET}")
        return True  # Don't fail the check if npm is not available

    # Check if node_modules exist
    if not (frontend_path / "node_modules").exists():
        print(f"{YELLOW}Installing dependencies...{RESET}")
        result = subprocess.run(["npm", "ci"], cwd=frontend_path, capture_output=False)
        if result.returncode != 0:
            return False

    # Run ESLint
    result = subprocess.run(["npm", "run", "lint"], cwd=frontend_path, capture_output=False)

    return result.returncode == 0


def main():
    print(f"{BLUE}{'='*50}{RESET}")
    print(f"{BLUE}GrandFlow Sanity Check{RESET}")
    print(f"{BLUE}{'='*50}{RESET}")

    if fix_mode:
        print(f"{YELLOW}Running in FIX mode (Black will auto-format){RESET}")

    results = {}

    if should_check_backend:
        results["backend"] = check_backend()

    if should_check_frontend:
        results["frontend"] = check_frontend()

    # Summary
    print(f"\n{BLUE}{'='*50}{RESET}")
    print(f"{BLUE}SUMMARY{RESET}")
    print(f"{BLUE}{'='*50}{RESET}")

    for check_name, passed in results.items():
        status = f"{GREEN}✓ PASSED{RESET}" if passed else f"{RED}✗ FAILED{RESET}"
        print(f"  {check_name.upper()}: {status}")

    all_passed = all(results.values())

    if all_passed:
        print(f"\n{GREEN}All checks passed! 🎉{RESET}")
        return 0
    else:
        print(f"\n{RED}Some checks failed. See above for details.{RESET}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
