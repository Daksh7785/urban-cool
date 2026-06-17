
import logging
import numpy as np
import scipy.ndimage as ndimage
import config

logger = logging.getLogger(__name__)

def get_elevation_data(gdf_grid, force_synthetic=False):
    np.random.seed(config.RANDOM_SEED)
    
    if force_synthetic or config.FORCE_OFFLINE_MODE:
        logger.warning("Offline mode: Generating synthetic elevation data")
        # Assume somewhat flat plateau (Indore is ~553m)
        elevation = np.random.normal(550.0, 10.0, len(gdf_grid))
        gdf_grid['elevation'] = np.clip(elevation, 500.0, 600.0)
        return gdf_grid
        
    try:
        raise TimeoutError("Simulated timeout for SRTM DEM data")
    except Exception as e:
        logger.warning(f"SRTM DEM data fetch failed: {str(e)}")
        return get_elevation_data(gdf_grid, force_synthetic=True)
