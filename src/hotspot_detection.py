import os
import json
import logging
import numpy as np
import pandas as pd
import geopandas as gpd
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GroupKFold
from sklearn.metrics import r2_score, root_mean_squared_error, mean_absolute_error
from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestRegressor

from src import config

# Setup logging
config.setup_logging()
logger = logging.getLogger(__name__)

def run_hotspot_detection():
    logger.info("Initializing Phase 2: Hotspot Detection and Machine Learning...")
    
    # Set seed for reproducibility
    np.random.seed(config.CITY.random_seed)
    
    # 1. Load the preprocessed grid data
    if not os.path.exists(config.PATHS.grid_data_path):
        raise FileNotFoundError(f"Processed grid data not found at {config.PATHS.grid_data_path}. Run data_pipeline.py first.")
        
    gdf = gpd.read_file(config.PATHS.grid_data_path)
    logger.info(f"Loaded grid dataset with {len(gdf)} cells.")
    
    # 2. Compute LST anomaly (z-score normalized)
    lst_vals = gdf['lst'].values
    mean_lst = np.mean(lst_vals)
    std_lst = np.std(lst_vals)
    gdf['lst_anomaly'] = (lst_vals - mean_lst) / std_lst
    
    # 3. DBSCAN Spatial Clustering of Hotspots
    # Filter cells where lst_anomaly > 1.0 (significantly hot)
    hot_mask = gdf['lst_anomaly'] > 1.0
    hot_cells = gdf[hot_mask].copy()
    
    logger.info(f"Number of hot cells (LST anomaly > 1.0): {len(hot_cells)}")
    
    if len(hot_cells) > 0:
        coords = hot_cells[['x_utm', 'y_utm']].values
        # Use DBSCAN with fixed spatial parameters
        db = DBSCAN(eps=450.0, min_samples=10)
        hot_cells['cluster_id'] = db.fit_predict(coords)
        
        # Merge cluster IDs back to main GeoDataFrame
        gdf['hotspot_id'] = -1
        gdf.loc[hot_mask, 'hotspot_id'] = hot_cells['cluster_id']
    else:
        logger.warning("No cells meet LST anomaly > 1.0 threshold. Using top 10% hottest cells as fallback...")
        thresh = np.percentile(lst_vals, 90)
        hot_mask = gdf['lst'] > thresh
        hot_cells = gdf[hot_mask].copy()
        coords = hot_cells[['x_utm', 'y_utm']].values
        db = DBSCAN(eps=450.0, min_samples=10)
        hot_cells['cluster_id'] = db.fit_predict(coords)
        gdf['hotspot_id'] = -1
        gdf.loc[hot_mask, 'hotspot_id'] = hot_cells['cluster_id']
        
    unique_clusters = [c for c in np.unique(gdf['hotspot_id'].values) if c != -1]
    logger.info(f"DBSCAN detected {len(unique_clusters)} hotspots.")
    
    # 4. Supervised ML Training with Spatial Cross-Validation
    target_col = 'lst'
    feature_cols = [
        'ndvi', 'ndbi', 'ndwi', 'albedo', 
        'building_density', 'building_height', 'road_density', 
        'population_density', 'elevation', 'dist_water', 'dist_green'
    ]
    
    X = gdf[feature_cols].copy()
    y = gdf[target_col].copy()
    
    # Implement Spatial Blocking CV
    block_x = pd.cut(gdf['x_utm'], bins=3, labels=False)
    block_y = pd.cut(gdf['y_utm'], bins=3, labels=False)
    gdf['spatial_block'] = block_x * 3 + block_y
    
    groups = gdf['spatial_block'].values
    gkf = GroupKFold(n_splits=5)
    
    xgb_metrics = {'r2': [], 'rmse': [], 'mae': []}
    rf_metrics = {'r2': [], 'rmse': [], 'mae': []}
    
    scaler = StandardScaler()
    X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=feature_cols)
    
    logger.info("Running Spatial Cross-Validation...")
    for fold, (train_idx, val_idx) in enumerate(gkf.split(X, y, groups=groups)):
        X_train, y_train = X.iloc[train_idx], y.iloc[train_idx]
        X_val, y_val = X.iloc[val_idx], y.iloc[val_idx]
        
        X_train_s = X_scaled.iloc[train_idx]
        X_val_s = X_scaled.iloc[val_idx]
        
        # Train XGBoost
        xgb = XGBRegressor(n_estimators=100, max_depth=5, learning_rate=0.1, random_state=config.CITY.random_seed)
        xgb.fit(X_train, y_train)
        y_pred_xgb = xgb.predict(X_val)
        
        # Train Random Forest
        rf = RandomForestRegressor(n_estimators=100, max_depth=8, random_state=config.CITY.random_seed)
        rf.fit(X_train_s, y_train)
        y_pred_rf = rf.predict(X_val_s)
        
        xgb_metrics['r2'].append(r2_score(y_val, y_pred_xgb))
        xgb_metrics['rmse'].append(root_mean_squared_error(y_val, y_pred_xgb))
        xgb_metrics['mae'].append(mean_absolute_error(y_val, y_pred_xgb))
        
        rf_metrics['r2'].append(r2_score(y_val, y_pred_rf))
        rf_metrics['rmse'].append(root_mean_squared_error(y_val, y_pred_rf))
        rf_metrics['mae'].append(mean_absolute_error(y_val, y_pred_rf))
        
    logger.info("--- Model Validation (Spatial Block CV) ---")
    mean_r2 = float(np.mean(xgb_metrics['r2']))
    mean_rmse = float(np.mean(xgb_metrics['rmse']))
    mean_mae = float(np.mean(xgb_metrics['mae']))
    
    logger.info(f"XGBoost R2:   {mean_r2:.4f} +/- {np.std(xgb_metrics['r2']):.4f}")
    logger.info(f"XGBoost RMSE: {mean_rmse:.4f}°C")
    logger.info(f"XGBoost MAE:  {mean_mae:.4f}°C")
    logger.info(f"Random Forest R2:   {np.mean(rf_metrics['r2']):.4f} +/- {np.std(rf_metrics['r2']):.4f}")
    logger.info(f"Random Forest RMSE: {np.mean(rf_metrics['rmse']):.4f}°C")
    logger.info(f"Random Forest MAE:  {np.mean(rf_metrics['mae']):.4f}°C")
    
    # Check minimum acceptable R2
    if mean_r2 < 0.30:
        logger.warning(f"WARNING: Model validation R2 ({mean_r2:.4f}) is below minimum acceptable threshold (0.30)!")
        
    # Save model metrics to outputs/model_metrics.json
    metrics_report = {
        "r2": mean_r2,
        "rmse": mean_rmse,
        "mae": mean_mae
    }
    metrics_json_path = os.path.join(config.PATHS.reports_dir, "model_metrics.json")
    with open(metrics_json_path, 'w') as f:
        json.dump(metrics_report, f, indent=4)
    logger.info(f"Model metrics saved to: {metrics_json_path}")
    
    # Train final model on the entire dataset
    xgb_model = XGBRegressor(n_estimators=100, max_depth=5, learning_rate=0.1, random_state=config.CITY.random_seed)
    xgb_model.fit(X, y)
    
    # Save the trained model to disk as a pickle file (Phase 6 compliance)
    import pickle
    os.makedirs(config.PATHS.models_dir, exist_ok=True)
    with open(config.PATHS.model_path, 'wb') as f:
        pickle.dump(xgb_model, f)
    logger.info(f"Trained XGBoost model pickle saved to: {config.PATHS.model_path}")
    
    gdf['lst_pred_ml'] = xgb_model.predict(X)
    
    # 5. Run SHAP Driver Attribution with fallback
    shap_values_matrix = None
    try:
        import shap
        logger.info("Calculating SHAP values for driver attribution...")
        explainer = shap.TreeExplainer(xgb_model)
        shap_explanation = explainer(X)
        shap_values_matrix = shap_explanation.values
    except Exception as e:
        logger.warning(f"SHAP TreeExplainer failed or not fully compatible: {str(e)}.")
        logger.warning("Using gradient-based local attribution fallback.")
        
        importances = xgb_model.feature_importances_
        X_norm = (X - X.mean()) / X.std()
        correlations = X.corrwith(y)
        signed_importances = importances * np.sign(correlations.values)
        
        shap_values_matrix = np.zeros(X.shape)
        for i, col in enumerate(feature_cols):
            shap_values_matrix[:, i] = signed_importances[i] * X_norm[col].values
            
    # Assign SHAP values to columns
    for i, col in enumerate(feature_cols):
        gdf[f'shap_{col}'] = shap_values_matrix[:, i]
        
    # Generate outputs/shap_summary.png (Phase 7 compliance)
    import matplotlib.pyplot as plt
    try:
        plt.figure(figsize=(10, 6))
        import shap
        shap.summary_plot(shap_values_matrix, X, show=False)
        plt.tight_layout()
        shap_img_path = os.path.join(config.PATHS.reports_dir, "shap_summary.png")
        plt.savefig(shap_img_path, dpi=150)
        plt.close()
        logger.info(f"SHAP summary plot saved to: {shap_img_path}")
    except Exception as e:
        logger.warning(f"Failed to generate SHAP summary plot via shap library: {str(e)}. Generating fallback plot.")
        mean_abs_shaps_fallback = np.mean(np.abs(shap_values_matrix), axis=0)
        fallback_df = pd.DataFrame({
            "feature": feature_cols,
            "importance": mean_abs_shaps_fallback
        }).sort_values(by="importance", ascending=True)
        plt.figure(figsize=(10, 6))
        plt.barh(fallback_df['feature'], fallback_df['importance'], color='skyblue')
        plt.title("Mean Absolute SHAP Value (Fallback)")
        plt.xlabel("Mean |SHAP value| (LST impact in °C)")
        plt.tight_layout()
        shap_img_path = os.path.join(config.PATHS.reports_dir, "shap_summary.png")
        plt.savefig(shap_img_path, dpi=150)
        plt.close()
        logger.info(f"Fallback feature importance summary plot saved to: {shap_img_path}")

    # Generate outputs/feature_importance.csv
    mean_abs_shaps = np.mean(np.abs(shap_values_matrix), axis=0)
    importance_df = pd.DataFrame({
        "feature": feature_cols,
        "importance": mean_abs_shaps
    }).sort_values(by="importance", ascending=False)
    feat_imp_path = os.path.join(config.PATHS.reports_dir, "feature_importance.csv")
    importance_df.to_csv(feat_imp_path, index=False)
    logger.info(f"Feature importance saved to: {feat_imp_path}")
        
    # 6. Calculate Hotspot Centroids, Severity, and Driver breakdown
    hotspots_list = []
    
    for cluster_id in unique_clusters:
        cluster_mask = gdf['hotspot_id'] == cluster_id
        cluster_gdf = gdf[cluster_mask]
        
        # Safe centroid calculation without deprecation warning
        if hasattr(cluster_gdf.geometry, 'union_all'):
            centroid = cluster_gdf.geometry.union_all().centroid
        else:
            centroid = cluster_gdf.geometry.unary_union.centroid
            
        centroid_lon = centroid.x if gdf.crs.is_geographic else cluster_gdf['lon_center'].mean()
        centroid_lat = centroid.y if gdf.crs.is_geographic else cluster_gdf['lat_center'].mean()
        
        severity = float(cluster_gdf['lst'].mean())
        severity_anomaly = float(cluster_gdf['lst_anomaly'].mean())
        affected_pop = int(cluster_gdf['population_density'].sum())
        
        mean_shaps = {}
        for col in feature_cols:
            mean_shaps[col] = float(cluster_gdf[f'shap_{col}'].mean())
            
        sorted_drivers = sorted(mean_shaps.items(), key=lambda x: abs(x[1]), reverse=True)
        
        top_drivers_json = []
        for k, v in sorted_drivers[:5]:
            abs_sum = sum(abs(val) for val in mean_shaps.values())
            pct = (abs(v) / abs_sum * 100.0) if abs_sum > 0 else 0.0
            top_drivers_json.append({
                "feature": k,
                "shap_value": v,
                "contribution_pct": round(pct, 1),
                "effect": "Heating" if v > 0 else "Cooling"
            })
            
        hotspot_info = {
            "hotspot_id": int(cluster_id),
            "centroid_lon": float(centroid_lon),
            "centroid_lat": float(centroid_lat),
            "severity_score": round(severity, 2),
            "severity_anomaly": round(severity_anomaly, 2),
            "affected_population": affected_pop,
            "area_sq_meters": len(cluster_gdf) * 22500,  # 150m * 150m grid spacing
            "top_drivers": top_drivers_json
        }
        hotspots_list.append(hotspot_info)
        
    # Save hotspots data
    os.makedirs(os.path.dirname(config.PATHS.hotspots_path), exist_ok=True)
    with open(config.PATHS.hotspots_path, 'w') as f:
        json.dump(hotspots_list, f, indent=4)
        
    # Generate outputs/hotspot_driver_report.csv
    hotspot_drivers_rows = []
    for hs in hotspots_list:
        for driver in hs["top_drivers"]:
            hotspot_drivers_rows.append({
                "hotspot_id": hs["hotspot_id"],
                "feature": driver["feature"],
                "shap_value": driver["shap_value"],
                "contribution_pct": driver["contribution_pct"],
                "effect": driver["effect"]
            })
    hs_driver_df = pd.DataFrame(hotspot_drivers_rows)
    hs_report_path = os.path.join(config.PATHS.reports_dir, "hotspot_driver_report.csv")
    hs_driver_df.to_csv(hs_report_path, index=False)
    logger.info(f"Hotspot driver report saved to: {hs_report_path}")
        
    # Save modeled grid
    gdf.to_file(config.PATHS.modeled_grid_path, driver="GeoJSON")
    
    logger.info(f"Phase 2 complete. Hotspot results saved to: {config.PATHS.hotspots_path}")
    logger.info(f"Modeled grid with predictions saved to: {config.PATHS.modeled_grid_path}")
    
    return gdf, hotspots_list


if __name__ == "__main__":
    run_hotspot_detection()
