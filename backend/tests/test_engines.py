import pytest
from src.gis.geospatial_pipelines import GeospatialOrchestrator
from src.ml.physics_ai_engine import PhysicsAIEngine
from src.services.digital_twin_engine import DigitalTwinEngine
from src.services.intervention_engine import InterventionEngine
from src.services.copilot_engine import ClimateCopilot
from src.services.global_intelligence_engine import GlobalIntelligenceEngine

def test_geospatial_pipelines():
    orch = GeospatialOrchestrator()
    res = orch.run_all([0, 0, 1, 1])
    assert res["lst"]["crs"] == "EPSG:4326"
    assert res["ndvi"]["crs"] == "EPSG:4326"

def test_physics_ai():
    engine = PhysicsAIEngine()
    res = engine.select_best_model({})
    assert "best_model" in res

def test_digital_twin():
    engine = DigitalTwinEngine()
    decadal = engine.generate_decadal_forecast("Indore")
    assert "2050" in decadal
    
def test_intervention_engine():
    engine = InterventionEngine()
    res = engine.simulate_intervention("Tree Plantation", 1000)
    assert res["validation_status"] == "PHYSICALLY_VALIDATED"
    assert res["cooling_impact_celsius"] <= 1.5

def test_copilot():
    copilot = ClimateCopilot()
    res = copilot.query("How to stop heatwaves?")
    assert len(res["citations"]) > 0
    assert res["metrics"]["hallucination_risk"] < 0.1

def test_global_intelligence():
    engine = GlobalIntelligenceEngine()
    scores = engine.generate_scores("Madrid")
    assert 1 <= scores["Global_Ranking"] <= 500
    mayor = engine.run_ai_mayor_mode("Madrid")
    assert mayor["mode"] == "AI_MAYOR"
