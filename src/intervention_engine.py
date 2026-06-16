import os
import json
import logging
import numpy as np
import pandas as pd
import geopandas as gpd
import pulp

from src import config
from src import physics_model

# Setup logging
config.setup_logging()
logger = logging.getLogger(__name__)

def simulate_all_hotspot_interventions(gdf_path: str = None, hotspots_path: str = None) -> dict:
    """
    For each detected hotspot, simulates the 5 intervention types cell-by-cell.
    Computes average delta LST (°C) and total cost (INR) for each scenario.
    """
    logger.info("Simulating cooling interventions for all hotspots...")
    
    # Load paths from config if not provided
    gdf_path = gdf_path or config.PATHS.modeled_grid_path
    hotspots_path = hotspots_path or config.PATHS.hotspots_path
    
    if not os.path.exists(gdf_path) or not os.path.exists(hotspots_path):
        raise FileNotFoundError("Processed grid or hotspot results not found. Run previous phases first.")
        
    gdf = gpd.read_file(gdf_path)
    with open(hotspots_path, 'r') as f:
        hotspots = json.load(f)
        
    # Standard cell area at Indore resolution:
    # 150m * 150m = 22,500 m^2
    # In case resolution changes, calculate from grid size
    # Grid covers Indore bbox (~15.5km x 14.4km)
    min_lon, min_lat, max_lon, max_lat = config.CITY.bbox_gps
    # Quick UTM projection to calculate area
    # Convert cell bounds to meters
    cell_geom = gdf.geometry.iloc[0]
    # Projected coordinates are in meters, let's get cell bounds in UTM
    min_x, min_y, max_x, max_y = cell_geom.bounds
    cell_area = (max_x - min_x) * (max_y - min_y)
    logger.info(f"Calculated grid cell area: {cell_area:.2f} sq meters")
    
    # Intervention list
    intervention_types = ["cool_roof", "tree_canopy", "cool_pavement", "green_corridor", "combined"]
    
    # Structure: {hotspot_id: {intervention_type: {delta_lst, cost, feasible_fraction}}}
    results = {}
    
    for hs in hotspots:
        hs_id = hs['hotspot_id']
        logger.info(f"Simulating hotspot {hs_id} (severity: {hs['severity_score']:.2f}°C, pop: {hs['affected_population']})...")
        
        # Filter grid cells in this hotspot
        hs_mask = gdf['hotspot_id'] == hs_id
        hs_cells = gdf[hs_mask]
        num_cells = len(hs_cells)
        
        results[hs_id] = {}
        
        # If no cells in hotspot, skip
        if num_cells == 0:
            continue
            
        for itype in intervention_types:
            cell_deltas = []
            cell_costs = []
            feasible_count = 0
            
            for _, cell in hs_cells.iterrows():
                # Prepare input dict
                cell_dict = {
                    'albedo': float(cell['albedo']),
                    'ndvi': float(cell['ndvi']),
                    'building_density': float(cell['building_density']),
                    'building_height': float(cell['building_height']),
                    'road_density': float(cell['road_density']),
                    'population_density': float(cell['population_density'])
                }
                
                # Check feasibility
                is_feasible = False
                cost = 0.0
                intensity = 1.0  # 100% intensity
                
                if itype == "cool_roof":
                    # Feasible if there are buildings
                    if cell_dict['building_density'] > 0.05:
                        is_feasible = True
                        # Cost: paint building rooftops (80% rooftop fraction is paintable)
                        cost = cell_area * cell_dict['building_density'] * 0.80 * config.COSTS.cool_roof_per_m2 * intensity
                        
                elif itype == "tree_canopy":
                    # Feasible if there is unbuilt space
                    if cell_dict['building_density'] + cell_dict['road_density'] < 0.85:
                        is_feasible = True
                        # 30% vegetation cover expansion
                        canopy_area = cell_area * 0.30 * intensity
                        num_trees = canopy_area / config.COSTS.tree_canopy_m2
                        cost = num_trees * config.COSTS.tree_planted
                        
                elif itype == "cool_pavement":
                    # Feasible if there are roads
                    if cell_dict['road_density'] > 0.05:
                        is_feasible = True
                        # Treat road network (50% road area treated)
                        pave_area = cell_area * cell_dict['road_density'] * 0.50 * intensity
                        cost = pave_area * config.COSTS.cool_pavement_per_m2
                        
                elif itype == "green_corridor":
                    # Feasible if there is plenty of open space
                    if cell_dict['building_density'] + cell_dict['road_density'] < 0.60:
                        is_feasible = True
                        # Convert 15% of cell to park
                        park_area = cell_area * 0.15 * intensity
                        cost = park_area * config.COSTS.pocket_park_per_m2
                        
                elif itype == "combined":
                    # Feasible if both roof and pavement exist and we have space
                    if (cell_dict['building_density'] > 0.05 or cell_dict['road_density'] > 0.05) and (cell_dict['building_density'] + cell_dict['road_density'] < 0.90):
                        is_feasible = True
                        # Blend: 50% intensity for each
                        cost_roof = cell_area * cell_dict['building_density'] * 0.80 * config.COSTS.cool_roof_per_m2 * 0.50 * intensity
                        canopy_area = cell_area * 0.30 * 0.50 * intensity
                        num_trees = canopy_area / config.COSTS.tree_canopy_m2
                        cost_trees = num_trees * config.COSTS.tree_planted
                        pave_area = cell_area * cell_dict['road_density'] * 0.50 * 0.50 * intensity
                        cost_pave = pave_area * config.COSTS.cool_pavement_per_m2
                        cost = cost_roof + cost_trees + cost_pave
                        
                if is_feasible:
                    feasible_count += 1
                    # Simulate delta LST using physics model
                    delta = physics_model.simulate_cooling_effect(cell_dict, itype, intensity)
                    cell_deltas.append(delta)
                    cell_costs.append(cost)
                else:
                    cell_deltas.append(0.0)
                    cell_costs.append(0.0)
                    
            feasible_fraction = feasible_count / num_cells
            # Average cooling across all cells (even non-feasible ones get 0.0 cooling, representing spatial dilution)
            avg_delta = float(np.mean(cell_deltas))
            total_cost = float(np.sum(cell_costs))
            
            results[hs_id][itype] = {
                "delta_lst": round(avg_delta, 2),
                "cost_inr": round(total_cost, 2),
                "feasible_fraction": round(feasible_fraction, 2),
                "is_feasible": feasible_fraction > 0.1  # feasible if at least 10% of cells can receive it
            }
            
    # Save simulated outcomes
    sim_path = os.path.join(config.PATHS.processed_data_dir, "intervention_simulations.json")
    with open(sim_path, 'w') as f:
        json.dump(results, f, indent=4)
    logger.info(f"Simulations complete. Saved results to: {sim_path}")
    
    return results

def solve_budget_optimization(budget: float, simulations: dict = None, hotspots_path: str = None) -> dict:
    """
    Solves the Multiple-Choice Knapsack Problem (MCKP) to select the optimal intervention 
    for each hotspot to maximize population-weighted cooling within a budget constraint.
    
    Falls back to a Greedy Knapsack solver if PuLP fails.
    """
    logger.info(f"Running budget optimization solver for budget = {budget:,.2f} INR...")
    
    hotspots_path = hotspots_path or config.PATHS.hotspots_path
    with open(hotspots_path, 'r') as f:
        hotspots = json.load(f)
        
    if simulations is None:
        sim_path = os.path.join(config.PATHS.processed_data_dir, "intervention_simulations.json")
        with open(sim_path, 'r') as f:
            simulations = json.load(f)
            
    # Standardise simulations keys to strings to prevent type mismatch
    simulations = {str(k): v for k, v in simulations.items()}
            
    # Build list of options
    # We want to select at most 1 intervention per hotspot
    # Options for hotspot i include: the 5 interventions and "no action" (cost=0, benefit=0)
    
    # Try solving with PuLP ILP
    try:
        prob = pulp.LpProblem("UHI_Mitigation_Optimization", pulp.LpMaximize)
        
        # Decision variables: x[i, j] = 1 if hotspot i gets intervention j
        x = {}
        options_map = {} # map variables to metadata
        
        for hs in hotspots:
            hs_id = str(hs['hotspot_id'])
            x[hs_id] = {}
            for j in simulations[hs_id].keys():
                sim = simulations[hs_id][j]
                if sim['is_feasible'] and sim['cost_inr'] > 0:
                    # pulp variable name
                    var_name = f"x_{hs_id}_{j}"
                    x[hs_id][j] = pulp.LpVariable(var_name, cat='Binary')
                    # Benefit: delta_lst * population * -1 (cooling is negative, make it positive benefit)
                    benefit = float(-sim['delta_lst'] * hs['affected_population'])
                    options_map[var_name] = {
                        "hotspot_id": int(hs_id),
                        "intervention": j,
                        "cost": sim['cost_inr'],
                        "delta_lst": sim['delta_lst'],
                        "benefit": benefit,
                        "population": hs['affected_population']
                    }
                    
        # Objective function: Maximize total benefit
        prob += pulp.lpSum(options_map[var_name]['benefit'] * x[hs_id][j] 
                           for hs_id in x.keys() for j in x[hs_id].keys() 
                           for var_name in [f"x_{hs_id}_{j}"] if var_name in options_map)
        
        # Constraint 1: Budget limit
        prob += pulp.lpSum(options_map[var_name]['cost'] * x[hs_id][j] 
                           for hs_id in x.keys() for j in x[hs_id].keys() 
                           for var_name in [f"x_{hs_id}_{j}"] if var_name in options_map) <= budget
        
        # Constraint 2: At most one selection per hotspot
        for hs_id in x.keys():
            prob += pulp.lpSum(x[hs_id][j] for j in x[hs_id].keys()) <= 1
            
        # Solve
        status = prob.solve(pulp.PULP_CBC_CMD(msg=False))
        
        if pulp.LpStatus[status] == "Optimal":
            logger.info("PuLP ILP optimizer found optimal solution.")
            portfolio = []
            total_spent = 0.0
            total_benefit = 0.0
            
            for hs_id in x.keys():
                for j in x[hs_id].keys():
                    if pulp.value(x[hs_id][j]) == 1:
                        var_name = f"x_{hs_id}_{j}"
                        opt = options_map[var_name]
                        portfolio.append({
                            "hotspot_id": opt['hotspot_id'],
                            "recommended_intervention": opt['intervention'],
                            "delta_lst_c": opt['delta_lst'],
                            "cost_inr": opt['cost'],
                            "population_benefited": opt['population']
                        })
                        total_spent += opt['cost']
                        total_benefit += opt['benefit']
            solver_type = "PuLP ILP"
            status_str = "Optimal"
        else:
            logger.warning(f"PuLP solver returned non-optimal status: {pulp.LpStatus[status]}. Falling back to greedy solver.")
            raise Exception("PuLP non-optimal")
            
    except Exception as e:
        logger.warning(f"PuLP optimization failed or solver unavailable ({str(e)}). Running Greedy solver fallback...")
        
        # Greedy Fallback Solver (Fractional approximation with Multiple-Choice constraints)
        flat_options = []
        for hs in hotspots:
            hs_id = str(hs['hotspot_id'])
            for j, sim in simulations[hs_id].items():
                if sim['is_feasible'] and sim['cost_inr'] > 0:
                    benefit = -sim['delta_lst'] * hs['affected_population']
                    cost = sim['cost_inr']
                    ratio = benefit / cost if cost > 0 else 0
                    flat_options.append({
                        "hotspot_id": int(hs_id),
                        "intervention": j,
                        "cost": cost,
                        "delta_lst": sim['delta_lst'],
                        "benefit": benefit,
                        "population": hs['affected_population'],
                        "ratio": ratio
                    })
                    
        # Sort options by efficiency ratio descending
        flat_options.sort(key=lambda x: x['ratio'], reverse=True)
        
        selected_hotspots = set()
        portfolio = []
        total_spent = 0.0
        total_benefit = 0.0
        
        for opt in flat_options:
            h_id = opt['hotspot_id']
            if h_id not in selected_hotspots and total_spent + opt['cost'] <= budget:
                selected_hotspots.add(h_id)
                portfolio.append({
                    "hotspot_id": h_id,
                    "recommended_intervention": opt['intervention'],
                    "delta_lst_c": opt['delta_lst'],
                    "cost_inr": opt['cost'],
                    "population_benefited": opt['population']
                })
                total_spent += opt['cost']
                total_benefit += opt['benefit']
                
        solver_type = "Greedy Knapsack (Fallback)"
        status_str = "Greedy-Feasible"

    # Force fallback if portfolio is empty (Phase 9 requirement: never return empty portfolio)
    if len(portfolio) == 0:
        logger.warning("Optimization portfolio is empty. Force-allocating cheapest option to highest temperature hotspot...")
        sorted_hs = sorted(hotspots, key=lambda x: x['severity_score'], reverse=True)
        for hs in sorted_hs:
            hs_id = str(hs['hotspot_id'])
            hs_sims = simulations[hs_id]
            cheapest_item = None
            cheapest_cost = float('inf')
            for j, sim in hs_sims.items():
                if sim['is_feasible'] and 0 < sim['cost_inr'] < cheapest_cost:
                    cheapest_cost = sim['cost_inr']
                    cheapest_item = (j, sim)
            if cheapest_item is not None:
                j, sim = cheapest_item
                portfolio.append({
                    "hotspot_id": int(hs_id),
                    "recommended_intervention": j,
                    "delta_lst_c": sim['delta_lst'],
                    "cost_inr": sim['cost_inr'],
                    "population_benefited": hs['affected_population']
                })
                total_spent += sim['cost_inr']
                total_benefit += -sim['delta_lst'] * hs['affected_population']
                break

    # Save to outputs/optimization_plan.csv (Phase 9 compliance)
    plan_rows = []
    for item in portfolio:
        cost = item["cost_inr"]
        temp_red = abs(item["delta_lst_c"])
        pop = item["population_benefited"]
        roi = (temp_red * pop) / cost if cost > 0 else 0.0
        
        plan_rows.append({
            "hotspot_id": item["hotspot_id"],
            "recommended_action": item["recommended_intervention"],
            "cost": cost,
            "temperature_reduction": temp_red,
            "roi": roi
        })
    plan_df = pd.DataFrame(plan_rows)
    plan_csv_path = os.path.join(config.PATHS.reports_dir, "optimization_plan.csv")
    plan_df.to_csv(plan_csv_path, index=False)
    logger.info(f"Optimization plan CSV saved to: {plan_csv_path}")

    return {
        "solver_type": solver_type,
        "status": status_str,
        "total_spent_inr": round(total_spent, 2),
        "total_cooling_benefit": round(total_benefit, 2),
        "portfolio": portfolio
    }


if __name__ == "__main__":
    # Test simulations if files exist
    try:
        sims = simulate_all_hotspot_interventions()
        opt_res = solve_budget_optimization(budget=2000000.0, simulations=sims)
        print("Optimization result portfolio size:", len(opt_res['portfolio']))
    except Exception as e:
        print("Setup error or files not present:", str(e))
