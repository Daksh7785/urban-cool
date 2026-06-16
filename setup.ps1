# PowerShell script to set up virtual environment and install dependencies on Windows
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "UrbanCool AI - Environment Setup for Windows (PowerShell)" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# Check Python installation
$pythonCheck = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCheck) {
    Write-Error "Python is not installed or not in your PATH. Please install Python 3.10+."
    exit 1
}

# Python version check
$pythonVersion = & python --version
Write-Host "[INFO] Detected Python Version: $pythonVersion" -ForegroundColor Yellow

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "[INFO] Creating Python virtual environment (venv)..." -ForegroundColor Yellow
    python -m venv venv
} else {
    Write-Host "[INFO] Virtual environment (venv) already exists." -ForegroundColor Yellow
}

# Activate virtual environment
Write-Host "[INFO] Activating virtual environment..." -ForegroundColor Yellow
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$activatePath = Join-Path $scriptDir "venv\Scripts\Activate.ps1"
if (Test-Path $activatePath) {
    . $activatePath
} else {
    Write-Error "Could not find activation script at $activatePath. Please activate manually: .\venv\Scripts\activate.ps1"
    exit 1
}

# Upgrade pip
Write-Host "[INFO] Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install dependencies
Write-Host "[INFO] Installing required packages from requirements.txt..." -ForegroundColor Yellow
pip install -r requirements.txt

# Verify setup
Write-Host "[INFO] Running verify_setup.py..." -ForegroundColor Yellow
python verify_setup.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Verification failed. Please check the dependencies." -ForegroundColor Red
    exit 1
}

Write-Host "[SUCCESS] Environment setup completed successfully!" -ForegroundColor Green
Write-Host "[INFO] To activate this environment in the future, run: .\venv\Scripts\Activate.ps1" -ForegroundColor Yellow
