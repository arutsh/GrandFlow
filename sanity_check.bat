@echo off
REM Sanity check script for GrandFlow (Windows)
REM Runs black, mypy, and flake8 on Python code

setlocal enabledelayedexpansion

REM Colors (using simple text indents for Windows CMD)
set "BLUE=[94m"
set "GREEN=[92m"
set "RED=[91m"
set "YELLOW=[93m"
set "RESET=[0m"

set "PROJECT_ROOT=%~dp0"
set "FIX_MODE=false"

REM Parse arguments
for %%A in (%*) do (
    if "%%A"=="--fix" set "FIX_MODE=true"
)

if "%FIX_MODE%"=="true" (
    echo Running in FIX mode (Black will auto-format)
)

echo.
echo ======================================
echo GrandFlow Sanity Check
echo ======================================
echo.

setlocal enabledelayedexpansion
set "BACKEND_PASSED=true"

REM Backend check
echo === BACKEND SANITY CHECK ===
echo.

for %%S in (users budget) do (
    echo Checking %%S service...
    
    set "SERVICE_PATH=%PROJECT_ROOT%services\%%S"
    set "PYTHONPATH=!SERVICE_PATH!;!SERVICE_PATH!\..\..\shared"
    
    REM Black
    echo Running black...
    if "%FIX_MODE%"=="true" (
        python -m black "!SERVICE_PATH!\app" >nul 2>&1
        if !errorlevel! equ 0 (
            echo [OK] Black passed
        ) else (
            set "BACKEND_PASSED=false"
        )
    ) else (
        python -m black --check "!SERVICE_PATH!\app" >nul 2>&1
        if !errorlevel! equ 0 (
            echo [OK] Black passed
        ) else (
            echo [FAILED] Black failed
            echo Hint: Run with --fix to auto-format
            set "BACKEND_PASSED=false"
        )
    )
    
    REM Mypy
    echo Running mypy...
    python -m mypy "!SERVICE_PATH!\app" >nul 2>&1
    if !errorlevel! equ 0 (
        echo [OK] Mypy passed
    ) else (
        echo [FAILED] Mypy failed
        set "BACKEND_PASSED=false"
    )
    
    REM Flake8
    echo Running flake8...
    python -m flake8 "!SERVICE_PATH!\app" >nul 2>&1
    if !errorlevel! equ 0 (
        echo [OK] Flake8 passed
    ) else (
        echo [FAILED] Flake8 failed
        set "BACKEND_PASSED=false"
    )
    
    echo.
)

REM Summary
echo ======================================
echo SUMMARY
echo ======================================
echo.

if "%BACKEND_PASSED%"=="true" (
    echo [OK] All checks passed!
    exit /b 0
) else (
    echo [FAILED] Some checks failed. See above for details.
    exit /b 1
)
