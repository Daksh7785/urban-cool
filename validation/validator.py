import os
import json
import logging
import geopandas as gpd
import numpy as np
from src import config

# Setup logging
config.setup_logging()
logger = logging.getLogger(__name__)

def validate_data(file_path: str = None) -> bool:
    """
    Validates the geospatial grid dataset.
    Checks:
    - Empty datasets
    - Invalid geometry
    - Invalid CRS
    - Missing columns
    - Invalid ranges for key attributes
    Outputs:
    - outputs/data_quality_report.json
    Returns True if critical checks pass, False otherwise.
    """
    logger.info("Initializing Data Quality Validation Layer...")
    
    file_path = file_path or config.PATHS.grid_data_path
    
    report = {
        "validation_status": "PASS",
        "file_inspected": os.path.basename(file_path),
        "total_rows": 0,
        "missing_values": {},
        "duplicate_rows": 0,
        "outliers": {},
        "failures": []
    }
    
    if not os.path.exists(file_path):
        msg = f"Data file does not exist: {file_path}"
        logger.error(msg)
        report["validation_status"] = "FAIL"
        report["failures"].append(msg)
        save_report(report)
        return False
        
    try:
        gdf = gpd.read_file(file_path)
    except Exception as e:
        msg = f"Failed to parse geospatial data file: {str(e)}"
        logger.error(msg)
        report["validation_status"] = "FAIL"
        report["failures"].append(msg)
        save_report(report)
        return False
        
    # 1. Empty dataset check
    report["total_rows"] = len(gdf)
    if len(gdf) == 0:
        msg = "Dataset is empty."
        logger.error(msg)
        report["validation_status"] = "FAIL"
        report["failures"].append(msg)
        save_report(report)
        return False
        
    # 2. Invalid CRS check
    expected_crs = config.CITY.utm_crs
    if gdf.crs is None or str(gdf.crs).lower() != expected_crs.lower():
        msg = f"Invalid CRS: found {gdf.crs}, expected {expected_crs}."
        logger.error(msg)
        report["validation_status"] = "FAIL"
        report["failures"].append(msg)
        
    # 3. Invalid geometry check
    invalid_geoms = (~gdf.geometry.is_valid).sum()
    empty_geoms = gdf.geometry.is_empty.sum()
    if invalid_geoms > 0 or empty_geoms > 0:
        msg = f"Found {invalid_geoms} invalid and {empty_geoms} empty geometries."
        logger.warning(msg)
        report["failures"].append(msg)
        
    # 4. Missing columns check
    required_cols = [
        'lst', 'ndvi', 'ndbi', 'albedo', 
        'building_density', 'building_height', 'road_density', 
        'population_density', 'elevation'
    ]
    missing_cols = [c for c in required_cols if c not in gdf.columns]
    if missing_cols:
        msg = f"Missing required columns: {missing_cols}"
        logger.error(msg)
        report["validation_status"] = "FAIL"
        report["failures"].append(msg)
        save_report(report)
        return False
        
    # 5. Missing values check
    for col in required_cols:
        missing_count = int(gdf[col].isna().sum())
        report["missing_values"][col] = missing_count
        if missing_count > 0:
            msg = f"Column '{col}' has {missing_count} missing values."
            logger.warning(msg)
            report["failures"].append(msg)
            
    # 6. Duplicate rows check (based on centroid coordinates)
    if 'x_utm' in gdf.columns and 'y_utm' in gdf.columns:
        dups = int(gdf.duplicated(subset=['x_utm', 'y_utm']).sum())
        report["duplicate_rows"] = dups
        if dups > 0:
            msg = f"Detected {dups} spatial coordinate duplicates."
            logger.warning(msg)
            report["failures"].append(msg)
            
    # 7. Invalid range checks & Outliers
    ranges = {
        'lst': (15.0, 55.0),
        'ndvi': (-1.0, 1.0),
        'ndbi': (-1.0, 1.0),
        'albedo': (0.0, 1.0),
        'building_density': (0.0, 1.0),
        'road_density': (0.0, 1.0)
    }
    
    for col, (vmin, vmax) in ranges.items():
        out_min = (gdf[col] < vmin).sum()
        out_max = (gdf[col] > vmax).sum()
        outliers_count = int(out_min + out_max)
        report["outliers"][col] = outliers_count
        
        if outliers_count > 0:
            msg = f"Column '{col}' has {outliers_count} values outside valid bounds [{vmin}, {vmax}]."
            logger.warning(msg)
            # Only fail if it's extremely severe (e.g. LST out of bounds)
            if col == 'lst':
                report["validation_status"] = "FAIL"
                report["failures"].append(msg)
            else:
                report["failures"].append(msg)
                
    save_report(report)
    
    if report["validation_status"] == "FAIL":
        logger.error("Data Quality Validation: FAILED.")
        return False
    else:
        logger.info("Data Quality Validation: PASSED.")
        return True

def save_report(report: dict):
    out_dir = config.PATHS.reports_dir
    os.makedirs(out_dir, exist_ok=True)
    report_path = os.path.join(out_dir, "data_quality_report.json")
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=4)
    logger.info(f"Data quality report exported to: {report_path}")

if __name__ == "__main__":
    validate_data()
