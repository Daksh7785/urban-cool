
import logging
import numpy as np
import config

logger = logging.getLogger(__name__)

def get_population_data(gdf_grid, force_synthetic=False):
    np.random.seed(config.RANDOM_SEED)
    
    if force_synthetic or config.FORCE_OFFLINE_MODE:
        logger.warning("Offline mode: Generating synthetic population data")
        b_density = gdf_grid.get('building_density', np.random.uniform(0, 1, len(gdf_grid)))
        pop_density = b_density * 15000.0 + np.random.normal(500, 300, len(gdf_grid))
        gdf_grid['population_density'] = np.clip(pop_density, 0.0, 50000.0)
        return gdf_grid
    
    try:
        raise TimeoutError("Simulated timeout for WorldPop data")
    except Exception as e:
        logger.warning(f"WorldPop data fetch failed: {str(e)}")
        return get_population_data(gdf_grid, force_synthetic=True)
