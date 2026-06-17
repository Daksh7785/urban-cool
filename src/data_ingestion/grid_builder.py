
import logging
import geopandas as gpd
from shapely.geometry import box
import config

logger = logging.getLogger(__name__)

def build_base_grid():
    logger.info("Building base analysis grid...")
    min_lat, min_lon, max_lat, max_lon = map(float, config.TARGET_BBOX.split(","))
    grid_size = config.GRID_MAX_CELLS
    
    d_lat = (max_lat - min_lat) / grid_size
    d_lon = (max_lon - min_lon) / grid_size
    
    polygons = []
    lats = []
    lons = []
    
    for i in range(grid_size):
        for j in range(grid_size):
            c_min_lat = min_lat + i * d_lat
            c_max_lat = c_min_lat + d_lat
            c_min_lon = min_lon + j * d_lon
            c_max_lon = c_min_lon + d_lon
            
            polygons.append(box(c_min_lon, c_min_lat, c_max_lon, c_max_lat))
            lats.append(c_min_lat + d_lat / 2.0)
            lons.append(c_min_lon + d_lon / 2.0)
            
    gdf = gpd.GeoDataFrame({
        'lat_center': lats,
        'lon_center': lons,
        'geometry': polygons
    }, crs="EPSG:4326")
    
    # Optional: project to UTM
    # gdf = gdf.to_crs(config.CITY.utm_crs)
    return gdf
