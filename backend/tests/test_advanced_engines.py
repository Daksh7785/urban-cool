import pytest
from src.services.advanced_simulation_engines import (
    GreenCorridorAI,
    CriticalInfrastructureProtector,
    EnergyDemandPredictor,
    ClimateJusticeEngine,
    FundingEngine,
    AutonomousClimateAgent
)

def test_green_corridor():
    ai = GreenCorridorAI()
    res = ai.identify_optimal_corridors({})
    assert len(res) > 0
    assert res[0]["trees_required"] > 0

def test_infrastructure():
    protector = CriticalInfrastructureProtector()
    res = protector.analyze_infrastructure("Indore")
    assert len(res) == 4
    assert "heat_risk_score" in res[0]

def test_energy_predictor():
    predictor = EnergyDemandPredictor()
    res = predictor.predict_demand()
    assert res["heatwave_demand_mw"] > res["current_demand_mw"]

def test_climate_justice():
    engine = ClimateJusticeEngine()
    res = engine.analyze_equity()
    assert "climate_justice_score" in res

def test_funding_engine():
    engine = FundingEngine()
    res = engine.match_funding(1000000)
    assert len(res["matched_funds"]) == 2

def test_autonomous_agent():
    agent = AutonomousClimateAgent()
    # It might return [] or alerts, just verify it runs
    res = agent.scan_and_alert()
    assert isinstance(res, list)
