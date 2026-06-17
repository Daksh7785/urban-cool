# Digital Twin Forecasting Engine
import random

class DigitalTwinEngine:
    def generate_decadal_forecast(self, city: str):
        return {
            "city": city,
            "Current State": {"temp": 38.5, "veg": 25.0, "urban": 60.0},
            "2030": {"temp": 39.2, "veg": 23.0, "urban": 65.0},
            "2040": {"temp": 40.1, "veg": 20.0, "urban": 72.0},
            "2050": {"temp": 41.5, "veg": 18.0, "urban": 80.0}
        }

    def generate_short_term_forecast(self, city: str):
        return {
            "24h": {"temp_peak": 40.1, "accuracy": 0.96},
            "72h": {"temp_peak": 39.5, "accuracy": 0.91},
            "7_Day": {"temp_peak": 42.0, "accuracy": 0.85},
            "30_Day": {"temp_peak": 44.5, "accuracy": 0.72}
        }
