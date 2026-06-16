# UrbanCool AI - Project Audit Report

This audit documents the current state, architecture, completed components, gaps/issues, and planned fixes for the **UrbanCool AI** Urban Heat Island (UHI) Mitigation system.

---

## 1. Current Architecture

UrbanCool AI is a modular geospatial decision support tool containing the following components:
1. **Configuration (`src/config.py`)**: Stores parameters (bounding boxes, meteorological parameters, physical constants, and file paths).
2. **Data Pipeline (`src/data_pipeline.py`)**: Responsible for obtaining spatial grids and downloading vectors (buildings, roads). Falls back to a deterministic, high-fidelity synthetic generator when offline.
3. **Hotspot Detection & ML (`src/hotspot_detection.py`)**: Uses DBSCAN to identify severe temperature anomalies (hotspots) and trains an XGBoost regressor (with a RandomForest fallback) using 5-fold Spatial Block Cross-Validation. Computes SHAP attributions for feature importance.
4. **Physics Model (`src/physics_model.py`)**: Implements the Oke surface energy balance model ($Rn = H + LE + G + Qa$) to validate ML predictions and simulate microclimate changes.
5. **Intervention Engine (`src/intervention_engine.py`)**: Evaluates cooling strategies (reflective roofs, trees, cool pavements, pocket parks) and runs a Multiple-Choice Knapsack budget optimization using PuLP (with a Greedy fallback).
6. **Dashboard (`dashboard/app.py`)**: Streamlit application exposing interactive maps, SHAP breakdown charts, and scenario simulators.
7. **End-to-End Test Suite (`tests/`)**: Smoke tests verifying pipeline logic and physical parameter ranges.

---

## 2. Audit Findings

### Completed Components
- **Core Python Modules**: Code files (`src/data_pipeline.py`, `src/hotspot_detection.py`, `src/physics_model.py`, `src/intervention_engine.py`) contain fully fleshed-out implementations of the core mathematical solvers (Brentq solver, PuLP ILP, DBSCAN, XGBoost cross-validation).
- **Offline Reliability**: The synthetic generator in `src/data_pipeline.py` correctly produces autocorrelated spatial LST maps, building layouts, and road networks.
- **Unit and Integration Tests**: Basic unit tests for the thermodynamic model and end-to-end smoke tests already exist.

### Incomplete or Non-Compliant Components & Gaps
1. **Missing central config constants**: The user request specifies a centralized `config.py` exposing top-level uppercase constants (`RANDOM_SEED`, `FORCE_OFFLINE_MODE`, `MAX_GRID_SIZE`, `MODEL_PATH`, `CACHE_PATH`, `LOG_PATH`, `EXPORT_PATH`, `HOTSPOT_PERCENTILE`, `DEFAULT_CITY`, `API_TIMEOUT`). The current `src/config.py` uses class-based config objects (e.g., `config.CITY.force_offline_mode`) instead.
2. **Missing `setup.ps1` and `setup.md`**: The repository currently has `setup.bat` and `setup.sh` but is missing the required PowerShell version (`setup.ps1`) and documentation markdown (`setup.md`).
3. **Unpinned dependency versions**: `requirements.txt` currently uses range specifiers (`numpy>=2.0.0`, `scipy>=1.10.0`, etc.) instead of pinning exact verified compatible versions.
4. **Validation Layer**: The user request requires a `validation/` directory/module that validates data (empty datasets, invalid geometry, invalid CRS, missing columns, invalid raster ranges) and outputs a detailed `outputs/data_quality_report.json`. This is currently missing or partially inline in `run_pipeline.py`.
5. **ML Cache Format & Metrics**: XGBoost serialization is done via `save_model` in JSON format. The user request requires generating `models/model.pkl` (pickle format) and writing a separate `outputs/model_metrics.json` containing $R^2$, RMSE, and MAE.
6. **Explainability Outputs**: The pipeline is missing tabular explainability dumps (`outputs/feature_importance.csv` and `outputs/hotspot_driver_report.csv`) and does not export the `outputs/shap_summary.png` plot.
7. **Budget Optimization Output**: The optimizer does not export `outputs/optimization_plan.csv`.
8. **Report Generation Library**: The dashboard's PDF exporter currently uses `matplotlib.pyplot.savefig` to write a PDF. The prompt explicitly requires using **`reportlab`** to generate `outputs/UrbanCool_Report.pdf` offline.
9. **Dashboard Navigation Names**: The dashboard navigation modes in `dashboard/app.py` use names like `🌆 City Map & Hotspots`, `📊 Heat Driver Analysis` instead of the requested exact sections (1. City Overview, 2. Hotspot Map, 3. Driver Analysis, 4. Intervention Simulator, 5. Budget Optimizer, 6. Transparency Panel).
10. **CI Workflow**: The `.github/workflows/ci.yml` file is missing.

---

## 3. Blockers
- **None**. The local Python environment is fully populated with working packages (XGBoost, Scipy, Geopandas, Streamlit, Matplotlib, PuLP, SHAP, etc.).

---

## 4. Remediation Plan

We will systematically refine and harden each component:
1. **Phase 1 (Environment)**: Pin all dependencies in `requirements.txt` to exact versions. Add `setup.ps1`, `setup.md`, and refine `verify_setup.py`.
2. **Phase 2 (Config)**: Refactor `src/config.py` to declare all required top-level uppercase constants and adapt import paths across all files.
3. **Phase 3 (Validation)**: Create `src/validation.py` to perform structural GIS validations and write `outputs/data_quality_report.json`.
4. **Phase 4 & 6 (ML Pipeline & Cache)**: Save models to `models/model.pkl` using pickle. Save metrics to `outputs/model_metrics.json`. Fail gracefully with warnings if $R^2 < 0.3$.
5. **Phase 7 (SHAP Explainability)**: Generate `outputs/shap_summary.png`, `outputs/feature_importance.csv`, and `outputs/hotspot_driver_report.csv`.
6. **Phase 8 & 9 (Physics & Optimization)**: Ensure cooling deltas are bounded. Save optimization plans to `outputs/optimization_plan.csv`.
7. **Phase 11 & 12 (Dashboard & ReportLab)**: Rename tabs to match the required structure. Implement the PDF exporter in `src/report_generator.py` using `reportlab`.
8. **Phase 13 & 14 (CI & Tests)**: Write `.github/workflows/ci.yml` and expand `tests/test_end_to_end.py`.
