import numpy as np
import pandas as pd
import json

def generate_forecast(current_temp):
    """2. Heat Forecast Engine: Simulates a 7-day LST forecast"""
    days = ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6", "Day 7"]
    # Introduce random walk for temperature forecast
    forecasts = [current_temp + np.random.normal(0, 1.5) for _ in range(7)]
    return dict(zip(days, forecasts))

def compute_uhvi(lst, population_density, ndvi):
    """3. Urban Heat Vulnerability Index: Combines hazard (LST), exposure (pop), and lack of adaptive capacity (-NDVI)"""
    # Normalize inputs (mock logic for demo purposes)
    norm_lst = min(max((lst - 25) / 20.0, 0), 1)
    norm_pop = min(max(population_density / 50000.0, 0), 1)
    norm_ndvi = min(max((ndvi + 1) / 2.0, 0), 1)
    
    uhvi = (0.5 * norm_lst) + (0.3 * norm_pop) + (0.2 * (1 - norm_ndvi))
    return min(uhvi, 1.0)

def generate_policy(hotspot_id, top_drivers):
    """4. Explainable Policy Engine: Auto-generates markdown policy"""
    policy = f"### Policy Recommendation for Hotspot {hotspot_id}\n\n"
    policy += "Based on our Explainable AI (SHAP) analysis, the following drivers are causing extreme heat:\n"
    for driver in top_drivers:
        feature = driver['feature']
        if feature == 'ndvi':
            policy += "- **Low Vegetation:** Immediate action required: Plant 500 drought-resistant trees.\n"
        elif feature == 'albedo':
            policy += "- **Low Albedo:** Mandate cool roof coatings for all commercial buildings in this zone.\n"
        elif feature == 'building_density':
            policy += "- **High Building Density:** Introduce wind corridors by modifying zoning laws for new constructions.\n"
    return policy

def compute_carbon_impact(intervention_type):
    """8. Carbon + Cooling Impact Analysis"""
    impacts = {
        "tree_canopy": {"carbon_sequestered_kg": 20, "embodied_carbon_kg": 5},
        "cool_roof": {"carbon_sequestered_kg": 0, "embodied_carbon_kg": 50},
        "cool_pavement": {"carbon_sequestered_kg": 0, "embodied_carbon_kg": 120}
    }
    return impacts.get(intervention_type, {"carbon_sequestered_kg": 0, "embodied_carbon_kg": 0})

def historical_evolution():
    """10. Historical Heat Evolution Analysis"""
    years = list(range(2014, 2025))
    base_temp = 35.0
    temps = [base_temp + (i * 0.15) + np.random.normal(0, 0.5) for i in range(len(years))]
    return dict(zip(years, temps))

def run_advanced_analytics(hotspots):
    results = {}
    for hs in hotspots:
        hid = hs['hotspot_id']
        results[hid] = {
            "forecast": generate_forecast(hs['mean_lst']),
            "uhvi_score": compute_uhvi(hs['mean_lst'], hs.get('affected_population', 10000), hs.get('mean_ndvi', 0.2)),
            "policy": generate_policy(hid, hs.get('top_drivers', [])),
            "historical_trend": historical_evolution()
        }
    return results
