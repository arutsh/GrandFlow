# Sanity Check Scripts

Quick code quality checks using Black, Mypy, and Flake8.

## Usage

### Python (Recommended - Cross-platform)
```bash
# Check code quality
python sanity_check.py

# Check backend only
python sanity_check.py --backend

# Check frontend only  
python sanity_check.py --frontend

# Fix Black formatting issues automatically
python sanity_check.py --fix

# Fix + Check backend only
python sanity_check.py --fix --backend
```

### Bash (Linux/Mac)
```bash
chmod +x sanity_check.sh

# Check code quality
./sanity_check.sh

# Fix Black formatting
./sanity_check.sh --fix
```

### Batch (Windows)
```cmd
# Check code quality
sanity_check.bat

# Fix Black formatting
sanity_check.bat --fix
```

## What Gets Checked

### Backend (Python)
- **Black**: Code formatting consistency
- **Mypy**: Static type checking
- **Flake8**: Code style and potential errors
- Applied to: `services/users/app` and `services/budget/app`

### Frontend (TypeScript/React)
- **ESLint**: Code linting
- Applied to: `frontend-typescript/`

## Requirements

Install development dependencies:
```bash
pip install black mypy flake8
npm install  # in frontend-typescript/
```

## Typical Workflow

1. **Before committing:**
   ```bash
   python sanity_check.py
   ```

2. **If Black finds issues:**
   ```bash
   python sanity_check.py --fix
   ```

3. **Fix remaining issues:**
   - Address Mypy type errors
   - Fix Flake8 linting issues
   - Then commit

## CI/CD Integration

These tools are automatically run in GitHub Actions (see `.github/workflows/main.yml`).

To ensure your changes pass CI, run locally before pushing:
```bash
python sanity_check.py
```
