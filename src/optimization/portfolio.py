
import logging
import pulp
import config
import os
import pandas as pd

logger = logging.getLogger(__name__)

def optimize_portfolio(budget, candidates):
    logger.info(f"Optimizing portfolio for budget {budget}...")
    
    if not candidates:
        return []
        
    # PuLP Knapsack
    prob = pulp.LpProblem("UrbanCool_Optimization", pulp.LpMaximize)
    
    # Variables
    x = {}
    for i, c in enumerate(candidates):
        x[i] = pulp.LpVariable(f"x_{i}", cat="Binary")
        
    # Objective: maximize total cooling benefit (delta_lst)
    prob += pulp.lpSum([x[i] * c['delta_lst'] for i, c in enumerate(candidates)])
    
    # Constraint: cost <= budget
    prob += pulp.lpSum([x[i] * c['cost'] for i, c in enumerate(candidates)]) <= budget
    
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    
    portfolio = []
    for i, c in enumerate(candidates):
        if pulp.value(x[i]) == 1.0:
            portfolio.append(c)
            
    # If budget too low for anything, return cheapest to prevent empty if budget was > 0
    if not portfolio and budget > 0:
        cheapest = min(candidates, key=lambda c: c['cost'])
        portfolio.append(cheapest)
        
    # Ensure non-empty fallback
    if not portfolio and candidates:
        portfolio.append(candidates[0])
        
    # Save plan
    pd.DataFrame(portfolio).to_csv(os.path.join(config.PATHS.reports_dir, "optimization_plan.csv"), index=False)
    
    return portfolio
