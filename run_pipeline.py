import os
import json
import logging
import time

import config
from src.utils.logging_config import setup_logging
from src.utils.validation import validate_pipeline_outputs

# Phase 1
from src.data_ingestion.grid_builder import build_base_grid
from src.data_ingestion.satellite import get_satellite_data
from src.data_ingestion.osm_features import get_osm_features
from src.data_ingestion.population import get_population_data
from src.data_ingestion.elevation import get_elevation_data

# Phase 2
from src.ml.hotspot_detection import detect_hotspots
from src.ml.feature_model import train_feature_model
from src.ml.explainability import generate_explainability

# Phase 3 & 4 (Setup interventions for later)
from src.physics.cooling_model import simulate_intervention
from src.optimization.portfolio import optimize_portfolio

logger = logging.getLogger(__name__)

def main():
    logger = setup_logging()
    logger.info("Starting UrbanCool AI Pipeline...")
    
    start_time = time.time()
    
    # Phase 1: Data Ingestion
    logger.info("Phase 1: Data Ingestion")
    gdf = build_base_grid()
    gdf = get_satellite_data(gdf)
    gdf = get_osm_features(gdf)
    gdf = get_population_data(gdf)
    gdf = get_elevation_data(gdf)
    
    gdf.to_file(config.PATHS.grid_data_path, driver="GeoJSON")
    logger.info("Grid data saved.")
    
    # Validation
    validate_pipeline_outputs()
    
    # Phase 2: ML
    logger.info("Phase 2: Machine Learning & Explainability")
    hotspots = detect_hotspots(gdf)
    
    model, features = train_feature_model(gdf)
    hotspots = generate_explainability(model, features, gdf, hotspots)
    
    with open(config.PATHS.hotspots_path, "w") as f:
        json.dump(hotspots, f, indent=4)
        
    # Phase 3 & 4 Simulation pre-computes for test suite
    logger.info("Phase 3 & 4: Physics and Optimization prep")
    candidates = []
    simulations = {}
    for hs in hotspots:
        hs_id = hs['hotspot_id']
        simulations[hs_id] = {}
        for itype in ["tree_canopy", "cool_roof", "cool_pavement"]:
            # simulate 20% coverage for base plan
            delta_lst, cost = simulate_intervention(itype, 20.0, hs['mean_lst'])
            
            simulations[hs_id][itype] = {
                'delta_lst': delta_lst,
                'cost_inr': cost
            }
            candidates.append({
                'hotspot_id': hs_id,
                'intervention': itype,
                'delta_lst': delta_lst,
                'cost': cost
            })
            
    with open(os.path.join(config.PATHS.processed_data_dir, "intervention_simulations.json"), "w") as f:
        json.dump(simulations, f, indent=4)
        
    portfolio = optimize_portfolio(5000000, candidates)
    
    # Phase 5 Report
    try:
        from src.report_generator import generate_report
        generate_report(gdf, hotspots, portfolio)
    except Exception as e:
        logger.warning(f"Report generation skipped/failed: {e}")
        
    logger.info(f"Pipeline finished in {time.time() - start_time:.2f}s")

if __name__ == "__main__":
    main()
