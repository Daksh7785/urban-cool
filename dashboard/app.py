import os
import time
import json
import logging
import numpy as np
import pandas as pd
import geopandas as gpd
import streamlit as st
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import plotly.express as px

import config
from src.physics.cooling_model import simulate_intervention
from src.optimization.portfolio import optimize_portfolio

st.set_page_config(page_title="UrbanCool AI", page_icon="❄️", layout="wide")

data_exists = (
    os.path.exists(config.PATHS.grid_data_path) and
    os.path.exists(config.PATHS.hotspots_path)
)

if not data_exists:
    st.info("No data found — running pipeline now")
    if st.button("🚀 Run Analysis Pipeline Now", type="primary", use_container_width=True):
        progress_bar = st.progress(0)
        st.write("Running pipeline...")
        import run_pipeline
        try:
            run_pipeline.main()
            st.success("Pipeline completed!")
            st.rerun()
        except Exception as e:
            st.error(f"Pipeline failed: {e}")
    st.stop()

@st.cache_data
def load_data():
    try:
        gdf = gpd.read_file(config.PATHS.grid_data_path)
        with open(config.PATHS.hotspots_path, 'r') as f:
            hotspots = json.load(f)
        return gdf, hotspots
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        st.stop()

gdf, hotspots = load_data()

app_mode = st.sidebar.radio("Navigation", [
    "1. City Overview",
    "2. Driver / Explainability Panel",
    "3. Intervention Simulator",
    "4. Budget-Prioritization Panel",
    "5. Transparency / About"
])

if app_mode == "1. City Overview":
    st.title("City Overview Map")
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        center_y = gdf.geometry.centroid.y.mean()
        center_x = gdf.geometry.centroid.x.mean()
        
    m = folium.Map(location=[center_y, center_x], zoom_start=12)
    
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        heat_data = [[row.geometry.centroid.y, row.geometry.centroid.x, row['lst']] for _, row in gdf.iterrows()]
        
    HeatMap(heat_data).add_to(m)
    for hs in hotspots:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            hs_y = gdf.iloc[hs['cell_indices'][0]].geometry.centroid.y
            hs_x = gdf.iloc[hs['cell_indices'][0]].geometry.centroid.x
            
        folium.CircleMarker(
            location=[hs_y, hs_x],
            radius=10, color='red', tooltip=f"Hotspot ID {hs['hotspot_id']}"
        ).add_to(m)
    st_folium(m, width=800, height=500)

elif app_mode == "2. Driver / Explainability Panel":
    st.title("Driver / Explainability Panel")
    selected_hs = st.selectbox("Select Hotspot", [h['hotspot_id'] for h in hotspots])
    hs = next(h for h in hotspots if h['hotspot_id'] == selected_hs)
    st.write(f"Mean LST: {hs['mean_lst']:.2f}C")
    if 'top_drivers' in hs:
        df = pd.DataFrame(hs['top_drivers'])
        fig = px.bar(df, x='contribution', y='feature', orientation='h', title='SHAP Attributions')
        st.plotly_chart(fig)

elif app_mode == "3. Intervention Simulator":
    st.title("Intervention Simulator")
    selected_hs = st.selectbox("Select Hotspot", [h['hotspot_id'] for h in hotspots])
    hs = next(h for h in hotspots if h['hotspot_id'] == selected_hs)
    
    col1, col2 = st.columns(2)
    with col1:
        tree_pct = st.slider("Tree Canopy %", 0, 50, 20)
        roof_pct = st.slider("Reflective Roof %", 0, 50, 0)
        pave_pct = st.slider("Permeable Pavement %", 0, 50, 0)
    
    with col2:
        try:
            total_delta = 0
            total_cost = 0
            if tree_pct > 0:
                d, c = simulate_intervention("tree_canopy", float(tree_pct), hs['mean_lst'])
                total_delta += d
                total_cost += c
            if roof_pct > 0:
                d, c = simulate_intervention("cool_roof", float(roof_pct), hs['mean_lst'])
                total_delta += d
                total_cost += c
            if pave_pct > 0:
                d, c = simulate_intervention("cool_pavement", float(pave_pct), hs['mean_lst'])
                total_delta += d
                total_cost += c
                
            st.metric("Total Cooling", f"{min(10.0, total_delta):.2f} C")
            st.metric("Total Cost", f"{total_cost:,.2f} INR")
        except Exception as e:
            st.error(f"Simulation error: {e}")

elif app_mode == "4. Budget-Prioritization Panel":
    st.title("Budget Optimizer")
    budget = st.number_input("Budget (INR)", min_value=0.0, value=5000000.0)
    
    try:
        with open(os.path.join(config.PATHS.processed_data_dir, "intervention_simulations.json"), "r") as f:
            sims = json.load(f)
            
        candidates = []
        for hs_id, data in sims.items():
            for itype, vals in data.items():
                candidates.append({
                    'hotspot_id': hs_id,
                    'intervention': itype,
                    'delta_lst': vals['delta_lst'],
                    'cost': vals['cost_inr']
                })
                
        if st.button("Optimize"):
            portfolio = optimize_portfolio(budget, candidates)
            if portfolio:
                st.dataframe(pd.DataFrame(portfolio))
            else:
                st.warning("Budget too low or no candidates.")
                
        if st.button("Export Report"):
            from src.report_generator import generate_report
            generate_report(gdf, hotspots, optimize_portfolio(budget, candidates))
            st.success(f"Report exported to {config.PATHS.report_path}")
            
    except Exception as e:
        st.error(f"Error loading simulations or optimizing: {e}")

elif app_mode == "5. Transparency / About":
    st.title("Transparency")
    st.write(f"**Data Sources Live/Synthetic**: Offline Mode is {config.FORCE_OFFLINE_MODE}.")
    st.write("All data generation currently falls back to synthetic representations for deterministic demo-safe functionality.")
    
    try:
        with open(os.path.join(config.PATHS.reports_dir, "model_metrics.json"), "r") as f:
            metrics = json.load(f)
        st.write(f"Model R2: {metrics.get('r2'):.2f}")
    except:
        st.write("Model metrics not found.")
