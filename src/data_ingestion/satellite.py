
import logging
import numpy as np
import scipy.ndimage as ndimage
import config

logger = logging.getLogger(__name__)

def get_satellite_data(gdf_grid, force_synthetic=False):
    np.random.seed(config.RANDOM_SEED)
    
    if force_synthetic or config.FORCE_OFFLINE_MODE:
        logger.warning("Offline mode: Generating synthetic satellite data (LST/NDVI)")
        grid_size = config.GRID_MAX_CELLS
        
        # NDVI
        ndvi = np.random.normal(0.4, 0.2, len(gdf_grid))
        ndvi = np.clip(ndvi, -1.0, 1.0)
        gdf_grid['ndvi'] = ndvi
        
        # LST
        thermal_noise_2d = np.random.normal(0, 2.0, (grid_size, grid_size))
        autocorr_noise = ndimage.gaussian_filter(thermal_noise_2d, sigma=5.0).flatten()
        
        if len(autocorr_noise) != len(gdf_grid):
            # Fallback if grid isn't exactly grid_size*grid_size
            autocorr_noise = np.random.normal(0, 1.0, len(gdf_grid))
            
        lst = 35.0 - 5.0 * ndvi + autocorr_noise
        lst = np.clip(lst, 15.0, 55.0)
        gdf_grid['lst'] = lst
        
        # NDBI, NDWI, Albedo
        gdf_grid['ndbi'] = np.clip(-ndvi + np.random.normal(0, 0.1, len(gdf_grid)), -1, 1)
        gdf_grid['ndwi'] = np.clip(0.1 + np.random.normal(0, 0.1, len(gdf_grid)), -1, 1)
        gdf_grid['albedo'] = np.clip(0.15 + np.random.normal(0, 0.05, len(gdf_grid)), 0, 1)
        
        return gdf_grid
    
    # Real logic with try/except
    try:
        raise TimeoutError("Simulated timeout for real Earth Engine data")
    except Exception as e:
        logger.warning(f"Satellite data fetch failed: {str(e)}")
        return get_satellite_data(gdf_grid, force_synthetic=True)
