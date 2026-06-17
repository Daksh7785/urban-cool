
import logging
import config

logger = logging.getLogger(__name__)

def simulate_intervention(intervention_type, magnitude, base_lst, cell_area=10000):
    # Returns delta_lst (between 0 and 10), and cost (>= 0)
    
    if intervention_type == "tree_canopy":
        # magnitude is % area
        delta_lst = (magnitude / 100.0) * 8.0 # max 8C cooling for 100% canopy
        trees_needed = (magnitude / 100.0 * cell_area) / config.COSTS.tree_canopy_m2
        cost = trees_needed * config.COSTS.tree_planted
        
    elif intervention_type == "cool_roof":
        delta_lst = (magnitude / 100.0) * 5.0 # max 5C cooling
        cost = (magnitude / 100.0 * cell_area) * config.COSTS.cool_roof_per_m2
        
    elif intervention_type == "cool_pavement":
        delta_lst = (magnitude / 100.0) * 4.0
        cost = (magnitude / 100.0 * cell_area) * config.COSTS.cool_pavement_per_m2
        
    else:
        delta_lst = 0.0
        cost = 0.0
        
    # Bounds check
    delta_lst = max(0.0, min(10.0, delta_lst))
    cost = max(0.0, cost)
    
    return delta_lst, cost
