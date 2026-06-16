import pytest
import numpy as np
from src import physics_model

def test_solver_convergence():
    """
    Test that the surface energy balance solver converges to a realistic temperature
    for standard urban/meteorological inputs.
    """
    ts = physics_model.solve_surface_temp(
        albedo=0.15,
        ndvi=0.2,
        building_density=0.5,
        building_height=10.0,
        population_density=5000.0,
        t_air=35.0,
        s_down=800.0,
        wind_speed=2.0,
        eps_air=0.75
    )
    # The temperature should be higher than air temperature (35°C) on a sunny day,
    # but within a physically plausible range (35°C to 65°C)
    assert 35.0 <= ts <= 65.0
    assert isinstance(ts, float)

def test_albedo_cooling():
    """
    Test that increasing albedo leads to a lower equilibrium temperature.
    """
    cell_data = {
        'albedo': 0.15,
        'ndvi': 0.2,
        'building_density': 0.5,
        'building_height': 15.0,
        'population_density': 5000.0
    }
    
    # Base temp
    t_base = physics_model.solve_surface_temp(
        albedo=cell_data['albedo'],
        ndvi=cell_data['ndvi'],
        building_density=cell_data['building_density'],
        building_height=cell_data['building_height'],
        population_density=cell_data['population_density']
    )
    
    # Increase albedo (e.g. paint roof)
    t_cool = physics_model.solve_surface_temp(
        albedo=0.45,  # higher albedo
        ndvi=cell_data['ndvi'],
        building_density=cell_data['building_density'],
        building_height=cell_data['building_height'],
        population_density=cell_data['population_density']
    )
    
    delta = t_cool - t_base
    assert delta < 0, f"Increasing albedo did not result in cooling! Delta: {delta}°C"
    assert -15.0 < delta < -0.5, f"Cooling delta {delta}°C is physically implausible."

def test_ndvi_cooling():
    """
    Test that increasing vegetation cover (NDVI) leads to a lower equilibrium temperature.
    """
    cell_data = {
        'albedo': 0.18,
        'ndvi': 0.2,
        'building_density': 0.4,
        'building_height': 10.0,
        'population_density': 3000.0
    }
    
    t_base = physics_model.solve_surface_temp(
        albedo=cell_data['albedo'],
        ndvi=cell_data['ndvi'],
        building_density=cell_data['building_density'],
        building_height=cell_data['building_height'],
        population_density=cell_data['population_density']
    )
    
    t_cool = physics_model.solve_surface_temp(
        albedo=cell_data['albedo'],
        ndvi=0.5,  # higher NDVI (more vegetation)
        building_density=cell_data['building_density'],
        building_height=cell_data['building_height'],
        population_density=cell_data['population_density']
    )
    
    delta = t_cool - t_base
    assert delta < 0, f"Increasing NDVI did not result in cooling! Delta: {delta}°C"
    assert -12.0 < delta < -0.2, f"Cooling delta {delta}°C is physically implausible."

def test_roughness_impact():
    """
    Test that increased building height/density increases roughness, reducing aerodynamic resistance ra,
    which enhances convective cooling (bringing Ts closer to T_air) when Ts > T_air.
    """
    # Hot surface (concrete roof baseline)
    t_smooth = physics_model.solve_surface_temp(
        albedo=0.15,
        ndvi=0.0,
        building_density=0.1,
        building_height=2.0,  # smooth
        population_density=0.0,
        t_air=35.0,
        s_down=800.0
    )
    
    t_rough = physics_model.solve_surface_temp(
        albedo=0.15,
        ndvi=0.0,
        building_density=0.6,
        building_height=20.0,  # rough
        population_density=0.0,
        t_air=35.0,
        s_down=800.0
    )
    
    # Rough urban canyons increase turbulence, reducing surface temperatures
    assert t_rough < t_smooth, f"Rougher surfaces should enhance sensible heat transfer, lowering Ts. Smooth: {t_smooth}, Rough: {t_rough}"
