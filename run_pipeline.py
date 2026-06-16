import logging
import os
import time
from src import config
from src.data_pipeline import run_data_pipeline
from src.hotspot_detection import run_hotspot_detection
from src.physics_model import validate_ml_predictions
from src.intervention_engine import simulate_all_hotspot_interventions, solve_budget_optimization
from src.report_generator import generate_pdf_report
from validation import validate_data

# Setup logging
config.setup_logging()
logger = logging.getLogger(__name__)

def execute_pipeline():
    logger.info("==================================================")
    logger.info("Running UrbanCool AI Comprehensive Pipeline...")
    logger.info("==================================================")
    
    # Stage 1: Data Acquisition
    logger.info("Stage 1/9: Running Data Acquisition...")
    run_data_pipeline(force_synthetic=config.CITY.force_offline_mode)
    
    # Stage 2: Data Validation
    logger.info("Stage 2/9: Running Data Validation...")
    is_valid = validate_data()
    if not is_valid:
        logger.error("Data validation failed! Pipeline aborting.")
        raise ValueError("Data validation check failed. See outputs/data_quality_report.json for details.")
        
    # Stages 3, 4, 5, 6: Feature Engineering, Hotspot Detection, ML Training, SHAP Explainability
    logger.info("Stages 3-6/9: Running Clustering, ML Model Training, & Attributions...")
    gdf, hotspots = run_hotspot_detection()
    
    # Stage 7: Physics Simulation (Thermodynamic validation)
    logger.info("Stage 7/9: Running Surface Energy Balance Validation...")
    gdf_validated = validate_ml_predictions(gdf)
    
    # Save validation columns to modeled grid (with retry loop for Windows file lock)
    for attempt in range(5):
        try:
            gdf_validated.to_file(config.PATHS.modeled_grid_path, driver="GeoJSON")
            break
        except PermissionError as e:
            if attempt == 4:
                raise e
            logger.warning(f"File lock collision on {config.PATHS.modeled_grid_path}. Retrying in 1.5s...")
            time.sleep(1.5)
    logger.info(f"Updated modeled grid with validation columns at: {config.PATHS.modeled_grid_path}")
    
    # Stage 8: Intervention simulations (What-if modeling)
    logger.info("Stage 8/9: Running Micro-climate Intervention Simulations...")
    sims = simulate_all_hotspot_interventions()
    
    # Stage 9: Optimization and PDF Report Export
    logger.info("Stage 9/9: Running Budget Optimization and PDF Artifact Export...")
    opt_res = solve_budget_optimization(budget=50000000.0, simulations=sims)
    generate_pdf_report(budget=50000000.0, opt_results=opt_res)
    
    logger.info("==================================================")
    logger.info("UrbanCool AI Pipeline Executed Successfully!")
    logger.info("All cache artifacts, metrics, and report PDFs are fully generated.")
    logger.info("To start the dashboard, run: streamlit run dashboard/app.py")
    logger.info("==================================================")

if __name__ == "__main__":
    execute_pipeline()
