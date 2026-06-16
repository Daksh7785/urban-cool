import os
import sys
import json
import numpy as np
import geopandas as gpd

from src import config

def test_pipeline():
    results = {}
    
    # 1. Check data validation report and input geometries
    try:
        report_path = os.path.join(config.PATHS.reports_dir, "data_quality_report.json")
        if os.path.exists(report_path):
            with open(report_path, 'r') as f:
                rep = json.load(f)
            if rep["validation_status"] == "PASS":
                results["Data Quality Check"] = ("PASS", "data_quality_report.json states status is PASS.")
            else:
                results["Data Quality Check"] = ("FAIL", f"Data quality validation failed: {rep['failures']}")
        else:
            results["Data Quality Check"] = ("FAIL", "data_quality_report.json not found.")
    except Exception as e:
        results["Data Quality Check"] = ("FAIL", f"Failed to verify quality report: {str(e)}")

    # 2. Assert processed data files exist
    if os.path.exists(config.PATHS.grid_data_path):
        results["Grid File Existence"] = ("PASS", "grid_data.geojson exists.")
    else:
        results["Grid File Existence"] = ("FAIL", "grid_data.geojson not found.")
        
    # 3. Check LST and NDVI ranges
    try:
        gdf = gpd.read_file(config.PATHS.grid_data_path)
        lst_min, lst_max = gdf['lst'].min(), gdf['lst'].max()
        ndvi_min, ndvi_max = gdf['ndvi'].min(), gdf['ndvi'].max()
        
        if 15.0 <= lst_min and lst_max <= 55.0:
            results["LST Range Check"] = ("PASS", f"LST range ({lst_min:.1f}°C - {lst_max:.1f}°C) is sane.")
        else:
            results["LST Range Check"] = ("FAIL", f"LST range ({lst_min:.1f}°C - {lst_max:.1f}°C) is out of bounds.")
            
        if -1.0 <= ndvi_min and ndvi_max <= 1.0:
            results["NDVI Range Check"] = ("PASS", f"NDVI range ({ndvi_min:.2f} - {ndvi_max:.2f}) is sane.")
        else:
            results["NDVI Range Check"] = ("FAIL", f"NDVI range ({ndvi_min:.2f} - {ndvi_max:.2f}) is out of bounds.")
    except Exception as e:
        results["Grid Data Verification"] = ("FAIL", f"Failed to check ranges: {str(e)}")
        
    # 4. Check Hotspot Count
    try:
        with open(config.PATHS.hotspots_path, 'r') as f:
            hotspots = json.load(f)
        num_hotspots = len(hotspots)
        if 1 <= num_hotspots <= 20:
            results["Hotspot Count Check"] = ("PASS", f"{num_hotspots} hotspots detected (sane).")
        else:
            results["Hotspot Count Check"] = ("FAIL", f"{num_hotspots} hotspots detected (out of bounds).")
            
        # Check SHAP driver attributions
        shap_passed = True
        for hs in hotspots:
            if len(hs.get("top_drivers", [])) == 0:
                shap_passed = False
        if shap_passed:
            results["SHAP Drivers Check"] = ("PASS", "All hotspots have attributed drivers in hotspots list.")
        else:
            results["SHAP Drivers Check"] = ("FAIL", "Some hotspots missing drivers in hotspots list.")
    except Exception as e:
        results["Hotspot Verification"] = ("FAIL", f"Failed to check hotspots: {str(e)}")

    # 5. Check ML Model and Metrics
    if os.path.exists(config.MODEL_PATH):
        results["Model Pickle Existence"] = ("PASS", "model.pkl exists.")
    else:
        results["Model Pickle Existence"] = ("FAIL", "model.pkl not found.")

    try:
        metrics_path = os.path.join(config.PATHS.reports_dir, "model_metrics.json")
        if os.path.exists(metrics_path):
            with open(metrics_path, 'r') as f:
                metrics = json.load(f)
            results["Model Metrics Check"] = ("PASS", f"model_metrics.json verified (R2={metrics.get('r2'):.4f}, RMSE={metrics.get('rmse'):.2f}).")
        else:
            results["Model Metrics Check"] = ("FAIL", "model_metrics.json not found.")
    except Exception as e:
        results["Model Metrics Check"] = ("FAIL", f"Failed to check model metrics: {str(e)}")

    # 6. Check Explainability CSV Outputs
    feat_imp_path = os.path.join(config.PATHS.reports_dir, "feature_importance.csv")
    hs_driver_path = os.path.join(config.PATHS.reports_dir, "hotspot_driver_report.csv")
    shap_summary_path = os.path.join(config.PATHS.reports_dir, "shap_summary.png")

    if os.path.exists(feat_imp_path) and os.path.exists(hs_driver_path) and os.path.exists(shap_summary_path):
        results["Explainability Outputs Check"] = ("PASS", "SHAP summary image and feature/hotspot driver CSV reports exist.")
    else:
        results["Explainability Outputs Check"] = ("FAIL", "Missing some explainability outputs (csv/png).")

    # 7. Check Physics Simulation plausibility
    try:
        simulations_path = os.path.join(config.PATHS.processed_data_dir, "intervention_simulations.json")
        with open(simulations_path, 'r') as f:
            sims = json.load(f)
            
        sim_passed = True
        for hs_id, hs_sims in sims.items():
            for itype, sim in hs_sims.items():
                cost = sim['cost_inr']
                delta = sim['delta_lst']
                # Cost must be non-negative, and absolute delta cooling must be <= 10.0
                if cost < 0 or not (0.0 <= abs(delta) <= 10.0):
                    sim_passed = False
                    
        if sim_passed:
            results["Physics Simulation Check"] = ("PASS", "Cooling deltas and costs are physically consistent (0 <= dT <= 10).")
        else:
            results["Physics Simulation Check"] = ("FAIL", "Implausible deltas or negative costs detected in simulations.")
    except Exception as e:
        results["Physics Simulation Check"] = ("FAIL", f"Failed to check simulations: {str(e)}")

    # 8. Check Optimization Plan
    opt_plan_path = os.path.join(config.PATHS.reports_dir, "optimization_plan.csv")
    if os.path.exists(opt_plan_path):
        try:
            import pandas as pd
            plan_df = pd.read_csv(opt_plan_path)
            if len(plan_df) > 0:
                results["Optimization Plan Check"] = ("PASS", f"optimization_plan.csv exists and is non-empty (rows={len(plan_df)}).")
            else:
                results["Optimization Plan Check"] = ("FAIL", "optimization_plan.csv is empty.")
        except Exception as e:
            results["Optimization Plan Check"] = ("FAIL", f"Failed to parse optimization_plan.csv: {str(e)}")
    else:
        results["Optimization Plan Check"] = ("FAIL", "optimization_plan.csv not found.")

    # 9. Check ReportLab PDF Exporter
    if os.path.exists(config.PATHS.report_path):
        results["PDF Report Existence"] = ("PASS", "UrbanCool_Report.pdf generated successfully.")
    else:
        results["PDF Report Existence"] = ("FAIL", "UrbanCool_Report.pdf not found.")

    # 10. Import app.py to check syntax
    try:
        import dashboard.app
        results["Dashboard Syntax Check"] = ("PASS", "dashboard/app.py imported successfully.")
    except Exception as e:
        results["Dashboard Syntax Check"] = ("FAIL", f"Dashboard import failed: {str(e)}")
        
    # Print PASS/FAIL summary table
    print("\n" + "="*80)
    print(f"{'SMOKE TEST MODULE':<40} | {'STATUS':<8} | {'DETAILS'}")
    print("="*80)
    all_passed = True
    for test_name, (status, details) in results.items():
        color_status = f"\033[92m{status:<8}\033[0m" if status == "PASS" else f"\033[91m{status:<8}\033[0m"
        print(f"{test_name:<40} | {color_status} | {details}")
        if status == "FAIL":
            all_passed = False
    print("="*80 + "\n")
    
    if all_passed:
        print("ALL TESTS PASSED SUCCESSFULLY! PROJECT IS DEMO-READY.")
        sys.exit(0)
    else:
        print("SOME TESTS FAILED! PLEASE REVIEW ISSUES.")
        sys.exit(1)

if __name__ == "__main__":
    test_pipeline()
