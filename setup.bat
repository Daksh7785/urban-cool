@echo off
echo ==========================================
echo UrbanCool AI - Environment Setup for Windows
echo ==========================================

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH. Please install Python 3.10+.
    exit /b 1
)

if not exist "venv" (
    echo [INFO] Creating Python virtual environment (venv)...
    python -m venv venv
) else (
    echo [INFO] Virtual environment (venv) already exists.
)

echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

echo [INFO] Upgrading pip...
python -m pip install --upgrade pip

echo [INFO] Installing required packages from requirements.txt...
pip install -r requirements.txt

echo [INFO] Running verify_setup.py...
python verify_setup.py

if %errorlevel% neq 0 (
    echo [ERROR] Verification failed. Please check the dependencies.
    exit /b 1
)

echo [SUCCESS] Environment setup completed successfully!
echo [INFO] To activate the environment in the future, run: call venv\Scripts\activate
