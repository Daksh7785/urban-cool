import logging
import numpy as np
import pandas as pd
import geopandas as gpd
from scipy.optimize import brentq

from src import config

# Setup logging
logger = logging.getLogger(__name__)

def solve_surface_temp(
    albedo: float, 
    ndvi: float, 
    building_density: float, 
    building_height: float, 
    population_density: float,
    t_air: float = None, 
    s_down: float = None, 
    wind_speed: float = None, 
    eps_air: float = None
) -> float:
    """
    Numerically solves the simplified Urban Surface Energy Balance equation for the 
    equilibrium surface temperature Ts (in Celsius) using scipy.optimize.brentq.
    
    Equation: Rn(Ts) = H(Ts) + LE(Ts) + G(Ts) + Qa
    """
    # Load defaults from config if not provided
    t_air = t_air if t_air is not None else config.METEOROLOGY.t_air
    s_down = s_down if s_down is not None else config.METEOROLOGY.s_down
    wind_speed = wind_speed if wind_speed is not None else config.METEOROLOGY.wind_speed
    eps_air = eps_air if eps_air is not None else config.METEOROLOGY.eps_air
    
    # Constants from config
    sigma = config.PHYSICS.sigma
    rho_air = config.PHYSICS.rho_air
    cp_air = config.PHYSICS.cp_air
    eps_surface = config.PHYSICS.eps_surface
    
    # Pre-calculate air temperature in Kelvin
    t_air_k = t_air + 273.15
    
    # Residual equation as a function of surface temperature Ts in Celsius
    def residual(Ts_C):
        Ts_K = Ts_C + 273.15
        
        # 1. Net Shortwave Radiation
        # S_net = (1 - albedo) * S_down
        S_net = (1.0 - albedo) * s_down
        
        # 2. Net Longwave Radiation
        # L_down = eps_air * sigma * T_air^4
        # L_up = eps_surface * sigma * Ts^4
        L_down = eps_air * sigma * (t_air_k ** 4)
        L_up = eps_surface * sigma * (Ts_K ** 4)
        Rn = S_net + L_down - L_up
        
        # 3. Ground Heat Storage (G)
        # Fraction f_G represents thermal storage capacity of concrete vs soil.
        # f_G is higher for urban (no vegetation, ~0.4) and lower for vegetated (~0.1)
        # Source: Oke (1987) "Boundary Layer Climates"
        f_G = 0.4 * (1.0 - ndvi) + 0.1 * ndvi
        f_G = max(0.1, min(0.4, f_G))
        G = f_G * Rn
        
        # 4. Latent Heat Flux (LE)
        # Evaporative fraction (EF) represents proportion of available energy going to evapotranspiration.
        # Heavily driven by vegetation index (NDVI). EF = 0.8 * NDVI is a standard approximation.
        EF = 0.8 * ndvi
        EF = max(0.0, min(0.8, EF))
        LE = EF * (Rn - G)
        
        # 5. Sensible Heat Flux (H)
        # Roughness length z0 (approx 10% of building height scaled by density)
        z0 = 0.1 * building_height * building_density + 0.01
        z0 = max(0.01, min(3.0, z0))
        
        # Aerodynamic resistance ra (neutral stability assumption)
        # ra = ln(10/z0)^2 / (kappa^2 * wind_speed) where kappa = 0.4 (von Karman constant) -> kappa^2 = 0.16
        ra = (np.log(10.0 / z0)) ** 2 / (0.16 * wind_speed)
        ra = max(5.0, ra)  # Lower bound for aerodynamic stability
        
        H = rho_air * cp_air * (Ts_C - t_air) / ra
        
        # 6. Anthropogenic Heat Flux (Qa)
        # Modeled as a function of population density and building density (waste heat from AC/traffic/industry)
        Qa = 0.002 * population_density + 20.0 * building_density
        
        # Balance: Rn - H - LE - G - Qa = 0
        return Rn - H - LE - G - Qa

    # Solve numerically using Brentq
    try:
        # Check boundary signs
        f_low = residual(t_air - 15.0)
        f_high = residual(t_air + 40.0)
        
        if f_low * f_high < 0:
            sol = brentq(residual, t_air - 15.0, t_air + 40.0)
        else:
            # Fallback: if bounds do not bracket the root, expand or pick the closest edge
            if abs(f_low) < abs(f_high):
                sol = t_air - 15.0
            else:
                sol = t_air + 40.0
    except Exception as e:
        logger.warning(f"Brentq solver failed to converge: {str(e)}. Using standard physical approximation.")
        # Fallback linear approximation: surface temp is higher in dense urban, lower in vegetated
        sol = t_air + 8.0 * building_density - 5.0 * ndvi
        
    return float(sol)

def validate_ml_predictions(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Computes physical surface temperatures for all grid cells and validates the 
    machine learning model's predictions. Flags thermodynamically inconsistent predictions.
    """
    logger.info("Running thermodynamics validation layer...")
    
    lst_physics_list = []
    
    # Extract values for calculation
    albedo_vals = gdf['albedo'].values
    ndvi_vals = gdf['ndvi'].values
    bd_vals = gdf['building_density'].values
    bh_vals = gdf['building_height'].values
    pd_vals = gdf['population_density'].values
    
    for i in range(len(gdf)):
        ts_phys = solve_surface_temp(
            albedo=albedo_vals[i],
            ndvi=ndvi_vals[i],
            building_density=bd_vals[i],
            building_height=bh_vals[i],
            population_density=pd_vals[i]
        )
        lst_physics_list.append(ts_phys)
        
    gdf['lst_physics'] = lst_physics_list
    
    # Calculate difference and confidence
    gdf['lst_diff'] = np.abs(gdf['lst'] - gdf['lst_physics'])
    
    # Confidence score ranges from 0 (very bad) to 1 (perfect agreement)
    gdf['lst_confidence'] = 1.0 - np.clip(gdf['lst_diff'] / 10.0, 0.0, 1.0)
    
    # Flag cells where the ML temperature differs from physics by > 5°C
    gdf['thermodynamically_consistent'] = gdf['lst_diff'] <= 5.0
    
    consistency_rate = gdf['thermodynamically_consistent'].mean() * 100.0
    logger.info(f"Thermodynamic validation complete. Consistency rate: {consistency_rate:.2f}%")
    
    return gdf

def simulate_cooling_effect(
    cell_data: dict, 
    intervention_type: str, 
    intensity: float
) -> float:
    """
    Simulates the cooling effect of a micro-climate intervention on a single cell.
    Returns the physical temperature drop delta LST (Celsius), which is negative or zero.
    """
    # 1. Solve base temperature
    t_base = solve_surface_temp(
        albedo=cell_data['albedo'],
        ndvi=cell_data['ndvi'],
        building_density=cell_data['building_density'],
        building_height=cell_data['building_height'],
        population_density=cell_data['population_density']
    )
    
    # 2. Modify parameters based on intervention type and intensity (0.0 to 1.0)
    albedo_new = cell_data['albedo']
    ndvi_new = cell_data['ndvi']
    building_density_new = cell_data['building_density']
    building_height_new = cell_data['building_height']
    population_density_new = cell_data['population_density']
    
    if intervention_type == "cool_roof":
        # Cool/Reflective Roof: Increase albedo of the building fraction of the cell
        # Standard roof: 0.15 albedo. Cool roof: 0.65 albedo (delta = 0.50)
        # Apply paint on building rooftops (assume 80% roof coverage is treatable)
        roof_delta = 0.50 * 0.80 * intensity
        albedo_new = cell_data['albedo'] + cell_data['building_density'] * roof_delta
        albedo_new = min(0.65, albedo_new)
        
    elif intervention_type == "tree_canopy":
        # Tree Canopy Expansion: Increase NDVI, representing vegetation cover expansion
        # A maximum 30% (+0.30) NDVI increase in the cell at 100% intensity
        ndvi_delta = 0.30 * intensity
        ndvi_new = cell_data['ndvi'] + ndvi_delta
        ndvi_new = min(0.85, ndvi_new)
        
    elif intervention_type == "cool_pavement":
        # Cool/Permeable Pavement: Increase road albedo, reduce storage fraction f_G, and increase soil moisture
        # Paint roads/pavement (road_density). Standard road: 0.12. Cool road: 0.30 (delta = 0.18)
        road_delta = 0.18 * intensity
        albedo_new = cell_data['albedo'] + cell_data['road_density'] * road_delta
        albedo_new = min(0.30, albedo_new)
        
        # Model pavement benefit by reducing thermal admittance (effectively lowering f_G)
        # Lowering f_G by up to 0.10 * road_density
        # This will be solved internally by solve_surface_temp using NDVI. 
        # To model the pavement heat absorption drop directly, we can add a pavement factor.
        # But to remain clean, we can simulate pavement as a slight local NDVI surrogate (soil moisture increase)
        ndvi_new = cell_data['ndvi'] + 0.10 * cell_data['road_density'] * intensity
        ndvi_new = min(0.80, ndvi_new)
        
    elif intervention_type == "green_corridor":
        # Green Corridor / Pocket Park: Significant vegetation and albedo boost in open spaces
        # Increases NDVI by 0.25 and ensures minimum albedo is 0.20
        ndvi_new = cell_data['ndvi'] + 0.25 * intensity
        ndvi_new = min(0.80, ndvi_new)
        albedo_new = max(cell_data['albedo'], 0.20)
        
    elif intervention_type == "combined":
        # Combined: Mixed strategy (50% cool roof, 50% tree canopy, 50% cool pavement)
        roof_delta = 0.50 * 0.80 * 0.5 * intensity
        albedo_new = cell_data['albedo'] + cell_data['building_density'] * roof_delta
        
        ndvi_delta = 0.30 * 0.5 * intensity
        ndvi_new = cell_data['ndvi'] + ndvi_delta
        ndvi_new = min(0.85, ndvi_new)
        
        road_delta = 0.18 * 0.5 * intensity
        albedo_new = albedo_new + cell_data['road_density'] * road_delta
        albedo_new = min(0.60, albedo_new)
        
    # 3. Solve new temperature
    t_new = solve_surface_temp(
        albedo=albedo_new,
        ndvi=ndvi_new,
        building_density=building_density_new,
        building_height=building_height_new,
        population_density=population_density_new
    )
    
    # Cooling delta is negative (cooling) or zero (no change)
    delta_lst = t_new - t_base
    abs_cooling = abs(delta_lst)
    
    # Enforce realistic limits: 0°C <= abs_cooling <= 10°C
    if not (0.0 <= abs_cooling <= 10.0):
        logger.warning(f"Unrealistic cooling delta computed: {delta_lst:.2f}°C. Rejecting and defaulting to 0.0°C.")
        return 0.0
        
    return min(0.0, delta_lst)


if __name__ == "__main__":
    # Test solver
    test_t = solve_surface_temp(albedo=0.15, ndvi=0.1, building_density=0.6, building_height=15.0, population_density=8000.0)
    print(f"Solved Test LST: {test_t:.2f}°C")
