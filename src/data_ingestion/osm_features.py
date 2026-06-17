
import logging
import numpy as np
import geopandas as gpd
from shapely.geometry import Polygon, LineString
import config

logger = logging.getLogger(__name__)

def get_osm_features(gdf_grid, force_synthetic=False):
    np.random.seed(config.RANDOM_SEED)
    
    if force_synthetic or config.FORCE_OFFLINE_MODE:
        logger.warning("Offline mode: Generating synthetic OSM data")
        
        b_density = np.clip(np.random.normal(0.4, 0.2, len(gdf_grid)), 0, 1)
        b_height = b_density * 20.0 + np.random.normal(0, 2.0, len(gdf_grid))
        b_height = np.clip(b_height, 0, 50)
        
        gdf_grid['building_density'] = b_density
        gdf_grid['building_height'] = b_height
        gdf_grid['road_density'] = np.clip(b_density * 0.8 + np.random.normal(0, 0.1, len(gdf_grid)), 0, 1)
        
        return gdf_grid
    
    try:
        raise TimeoutError("Simulated timeout for OSM data")
    except Exception as e:
        logger.warning(f"OSM data fetch failed: {str(e)}")
        return get_osm_features(gdf_grid, force_synthetic=True)
