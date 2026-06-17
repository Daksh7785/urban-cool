import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.physics.cooling_model import simulate_intervention

def test_physics():
    # Test 1: Zero intervention
    dlst, cost = simulate_intervention("tree_canopy", 0.0, 40.0)
    assert dlst == 0.0, "Delta LST must be 0 when intervention is 0"
    assert cost == 0.0, "Cost must be 0 when intervention is 0"
    
    # Test 2: Bounded dLST
    dlst, cost = simulate_intervention("cool_roof", 100.0, 40.0)
    assert 0.0 <= dlst <= 10.0, "Delta LST must be between 0 and 10"
    assert cost >= 0.0, "Cost must be positive"
    
    # Test 3: Monotonicity
    dlst1, cost1 = simulate_intervention("cool_pavement", 10.0, 40.0)
    dlst2, cost2 = simulate_intervention("cool_pavement", 50.0, 40.0)
    assert dlst2 > dlst1, "Delta LST should increase with magnitude"
    assert cost2 > cost1, "Cost should increase with magnitude"
    
    print("ALL PHYSICS TESTS PASSED")

if __name__ == "__main__":
    test_physics()
