import os
from pydantic import BaseModel, Field
from typing import Tuple

# ==============================================================================
# 0. CONFIGURATION — SET THIS FIRST
# ==============================================================================
TARGET_CITY        = "Indore, India"
# south, west, north, east lat/lon
TARGET_BBOX        = "22.65, 75.80, 22.75, 75.95"
CLIMATE_BASELINE   = "hot semi-arid, flat terrain, pre-monsoon summer peak ~42-45°C"
RANDOM_SEED        = 42
GRID_MAX_CELLS     = 100   # 100x100 max, configurable
FORCE_OFFLINE_MODE = True  # ship demo-safe by default

API_TIMEOUT = 30
HOTSPOT_PERCENTILE = 90

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_PATH = os.path.join(BASE_DIR, "data", "processed")
MODEL_PATH = os.path.join(BASE_DIR, "models", "model.pkl")
LOG_PATH = os.path.join(BASE_DIR, "logs", "pipeline.log")
EXPORT_PATH = os.path.join(BASE_DIR, "outputs", "UrbanCool_Report.pdf")

# Ensure required directories exist
os.makedirs(os.path.join(BASE_DIR, "data", "raw"), exist_ok=True)
os.makedirs(CACHE_PATH, exist_ok=True)
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
os.makedirs(os.path.dirname(EXPORT_PATH), exist_ok=True)
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

class CityConfig(BaseModel):
    name: str = TARGET_CITY
    bbox_gps: Tuple[float, float, float, float] = Field(
        default=(75.80, 22.65, 75.95, 22.75),
        description="Bounding Box (Min Lon, Min Lat, Max Lon, Max Lat) in EPSG:4326"
    )
    utm_crs: str = "EPSG:32643"  # UTM Zone 43N
    grid_res_cells: int = GRID_MAX_CELLS
    force_offline_mode: bool = FORCE_OFFLINE_MODE
    random_seed: int = RANDOM_SEED
    api_timeout: int = API_TIMEOUT
    climate_baseline: str = CLIMATE_BASELINE

class MeteorologyConfig(BaseModel):
    t_air: float = Field(default=35.0, description="Ambient air temperature in Celsius")
    s_down: float = Field(default=800.0, description="Downward shortwave solar radiation in W/m^2")
    wind_speed: float = Field(default=2.0, description="Wind speed at 10m height in m/s")
    eps_air: float = Field(default=0.75, description="Atmospheric emissivity (dimensionless)")

class PhysicsConstants(BaseModel):
    sigma: float = Field(default=5.67e-8, description="Stefan-Boltzmann constant in W/m^2/K^4")
    rho_air: float = Field(default=1.2, description="Density of air in kg/m^3")
    cp_air: float = Field(default=1005.0, description="Specific heat of air in J/kg/K")
    eps_surface: float = Field(default=0.95, description="Emissivity of urban surface (dimensionless)")

class CostConfig(BaseModel):
    cool_roof_per_m2: float = Field(default=150.0, description="Cool roof paint cost in INR/m^2")
    tree_planted: float = Field(default=500.0, description="Tree cost in INR (includes planting & maintenance)")
    tree_canopy_m2: float = Field(default=10.0, description="Average canopy area covered per tree in m^2")
    cool_pavement_per_m2: float = Field(default=800.0, description="Cool/permeable pavement cost in INR/m^2")
    pocket_park_per_m2: float = Field(default=1200.0, description="Green space landscaping cost in INR/m^2")

class PathConfig(BaseModel):
    base_dir: str = BASE_DIR
    raw_data_dir: str = os.path.join(base_dir, "data", "raw")
    processed_data_dir: str = CACHE_PATH
    models_dir: str = os.path.dirname(MODEL_PATH)
    reports_dir: str = os.path.dirname(EXPORT_PATH)
    logs_dir: str = os.path.dirname(LOG_PATH)
    
    grid_data_path: str = os.path.join(CACHE_PATH, "grid_data.geojson")
    modeled_grid_path: str = os.path.join(CACHE_PATH, "modeled_grid.geojson")
    hotspots_path: str = os.path.join(CACHE_PATH, "hotspot_results.json")
    model_path: str = MODEL_PATH
    report_path: str = EXPORT_PATH
    log_file_path: str = LOG_PATH

# Instantiate default configs for compatibility
CITY = CityConfig()
METEOROLOGY = MeteorologyConfig()
PHYSICS = PhysicsConstants()
COSTS = CostConfig()
PATHS = PathConfig()
