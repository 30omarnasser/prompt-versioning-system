# fix_and_run.ps1 - Updated version
Write-Host "Fixing configuration issues..." -ForegroundColor Cyan

# Stop any running processes on port 8000
Write-Host "Checking for processes on port 8000..." -ForegroundColor Yellow
$connections = netstat -ano | findstr :8000
if ($connections) {
    Write-Host "Found processes using port 8000. Stopping them..." -ForegroundColor Yellow
    $connections | ForEach-Object {
        $parts = $_ -split '\s+'
        $pid = $parts[-1]
        if ($pid -match '^\d+$') {
            Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
        }
    }
    Start-Sleep -Seconds 2
}

# Recreate virtual environment (clean install)
Write-Host "Recreating virtual environment..." -ForegroundColor Yellow
Remove-Item -Recurse -Force venv -ErrorAction SilentlyContinue
python -m venv venv

# Activate and install
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

Write-Host "Installing dependencies..." -ForegroundColor Yellow
python -m pip install --upgrade pip
pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic pydantic-settings python-dotenv aiohttp

# Create fresh .env file
Write-Host "Creating .env file..." -ForegroundColor Yellow
@"
DATABASE_URL=sqlite:///./prompt.db
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
DEFAULT_TEMPERATURE=0.7
LOG_LEVEL=INFO
"@ | Out-File -FilePath .env -Encoding utf8

# Note: Using SQLite for now to avoid PostgreSQL issues
Write-Host "Using SQLite database (no PostgreSQL needed)" -ForegroundColor Cyan

# Run the application
Write-Host "Starting application..." -ForegroundColor Green
Write-Host "API will be available at: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000