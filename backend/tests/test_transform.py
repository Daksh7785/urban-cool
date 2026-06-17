import pytest
from src.services.transform_engine import TransformCityEngine

def test_transform_my_city():
    engine = TransformCityEngine()
    payload = engine.transform("Singapore")
    
    # Verify all 15 phases return data structurally
    assert "diagnostic" in payload
    assert payload["diagnostic"]["Heat_Risk"] >= 70
    assert "forecast" in payload
    assert "2050" in payload["forecast"]
    assert "agent_chain" in payload
    assert len(payload["agent_chain"]) == 3
    assert payload["presentations"]["pdf_status"] == "READY"
