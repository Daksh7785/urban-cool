#!/bin/bash
echo "=========================================="
echo "UrbanCool AI - Environment Setup for Unix"
echo "=========================================="

OS="$(uname -s)"
echo "[INFO] Detected OS: $OS"

if [ "$OS" = "Linux" ]; then
    if command -v apt-get &> /dev/null; then
        echo "[INFO] Ubuntu/Debian detected. System libraries can be installed via:"
        echo "       sudo apt-get update && sudo apt-get install -y python3-dev gdal-bin libgdal-dev proj-bin libproj-dev"
    fi
elif [ "$OS" = "Darwin" ]; then
    if command -v brew &> /dev/null; then
        echo "[INFO] macOS detected. System libraries can be installed via:"
        echo "       brew install gdal proj"
    fi
fi

if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed or not in PATH. Please install Python 3.10+."
    exit 1
fi

if [ ! -d "venv" ]; then
    echo "[INFO] Creating Python virtual environment (venv)..."
    python3 -m venv venv
else
    echo "[INFO] Virtual environment (venv) already exists."
fi

echo "[INFO] Activating virtual environment..."
source venv/bin/activate

echo "[INFO] Upgrading pip..."
python3 -m pip install --upgrade pip

echo "[INFO] Installing required packages from requirements.txt..."
pip install -r requirements.txt

echo "[INFO] Running verify_setup.py..."
python verify_setup.py

if [ $? -ne 0 ]; then
    echo "[ERROR] Verification failed. Please check the dependencies."
    exit 1
fi

echo "[SUCCESS] Environment setup completed successfully!"
echo "[INFO] To activate the environment in the future, run: source venv/bin/activate"
