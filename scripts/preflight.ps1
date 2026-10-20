$ErrorActionPreference = "Stop"
Write-Host "TSI Agent Lab - Pre-flight" -ForegroundColor Cyan

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: uv no esta instalado o no esta en PATH." -ForegroundColor Red
    Write-Host 'Instale con: powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"'
    exit 1
}

uv --version
uv run python -c "import sys; print('Python:', sys.version.split()[0]); print('Interpreter:', sys.executable)"
Write-Host "Ejecutando quality gates..." -ForegroundColor Cyan
uv run ruff check .
uv run python -m pytest -q
Write-Host "Pre-flight completado." -ForegroundColor Green
