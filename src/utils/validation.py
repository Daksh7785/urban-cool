import os
import json
import logging
import pandas as pd
import geopandas as gpd
from src.utils.logging_config import setup_logging
import config

logger = logging.getLogger(__name__)

def check_bounds(val, min_val, max_val, name="Value"):
    if not (min_val <= val <= max_val):
        logger.warning(f"Validation Error: {name} ({val}) is out of bounds [{min_val}, {max_val}]")
        return False
    return True

def validate_pipeline_outputs():
    setup_logging()
    logger.info("Validating pipeline outputs...")
    failures = []
    
    # 1. Check Grid
    if not os.path.exists(config.PATHS.grid_data_path):
        failures.append("grid_data.geojson is missing.")
    else:
        gdf = gpd.read_file(config.PATHS.grid_data_path)
        if gdf.empty:
            failures.append("grid_data.geojson is empty.")
        if "lst" in gdf.columns:
            if gdf["lst"].min() < 15 or gdf["lst"].max() > 55:
                failures.append(f"LST out of bounds (15-55): {gdf['lst'].min()} to {gdf['lst'].max()}")
        if "ndvi" in gdf.columns:
            if gdf["ndvi"].min() < -1 or gdf["ndvi"].max() > 1:
                failures.append(f"NDVI out of bounds (-1 to 1): {gdf['ndvi'].min()} to {gdf['ndvi'].max()}")
                
    # write report
    report = {
        "validation_status": "PASS" if not failures else "FAIL",
        "failures": failures
    }
    
    report_path = os.path.join(config.PATHS.reports_dir, "data_quality_report.json")
    with open(report_path, "w") as f:
        json.dump(report, f, indent=4)
    
    if failures:
        logger.error(f"Validation failed: {failures}")
        return False
    logger.info("Validation passed.")
    return True
