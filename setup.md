# UrbanCool AI - Environment Setup Guide

This document describes the environment hardening, system dependencies, and steps to build the virtual environment for **UrbanCool AI**.

---

## 1. System Requirements

### Geospatial System Dependencies
UrbanCool AI uses advanced geospatial vector and raster libraries (`geopandas`, `shapely`, `pyogrio`, `scipy`). These libraries may require native binary distributions for GDAL and PROJ depending on your operating system.

- **Windows**: Binary dependencies are packaged directly within the Python wheels (e.g. `pyogrio` and `shapely`). No manual native compilation is necessary.
- **Linux (Ubuntu/Debian)**: Install packages via `apt-get`:
  ```bash
  sudo apt-get update && sudo apt-get install -y python3-dev gdal-bin libgdal-dev proj-bin libproj-dev
  ```
- **macOS**: Install via `Homebrew`:
  ```bash
  brew install gdal proj
  ```

---

## 2. Installation Steps

### Windows (PowerShell)
Execute the PowerShell installer script to automatically create a virtual environment, upgrade pip, install pinned versions from `requirements.txt`, and run verification:
```powershell
.\setup.ps1
```

### Windows (Command Prompt)
Alternatively, use the batch installer:
```cmd
setup.bat
```

### macOS / Linux
Run the bash script to configure the environment:
```bash
chmod +x setup.sh
./setup.sh
```

---

## 3. Environment Verification

To manually run verification checks to verify package integrity and version correctness, run:
```bash
python verify_setup.py
```

All status items must output `PASS` with the appropriate pinned version matching `requirements.txt`.
