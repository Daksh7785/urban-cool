
import logging
import numpy as np
import shap
import pandas as pd
import matplotlib.pyplot as plt
import config
import os

logger = logging.getLogger(__name__)

def generate_explainability(model, features, gdf_grid, hotspots):
    logger.info("Generating SHAP explainability...")
    
    X = gdf_grid[features].values
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)
    
    # Plot summary
    plt.figure()
    shap.summary_plot(shap_values, X, feature_names=features, show=False)
    plt.savefig(os.path.join(config.PATHS.reports_dir, "shap_summary.png"), bbox_inches='tight')
    plt.close()
    
    # Global feature importance
    mean_abs_shap = np.abs(shap_values).mean(axis=0)
    feat_imp_df = pd.DataFrame({'feature': features, 'importance': mean_abs_shap})
    feat_imp_df = feat_imp_df.sort_values('importance', ascending=False)
    feat_imp_df.to_csv(os.path.join(config.PATHS.reports_dir, "feature_importance.csv"), index=False)
    
    # Hotspot drivers
    hs_reports = []
    for hs in hotspots:
        idx = hs['cell_indices']
        hs_shap = shap_values[idx].mean(axis=0) # mean shap values for this hotspot
        top_driver_idx = np.argmax(hs_shap) # largest positive contributor to LST
        hs['top_drivers'] = [{'feature': features[top_driver_idx], 'contribution': float(hs_shap[top_driver_idx])}]
        hs_reports.append({
            'hotspot_id': hs['hotspot_id'],
            'top_driver': features[top_driver_idx],
            'contribution': float(hs_shap[top_driver_idx])
        })
        
    pd.DataFrame(hs_reports).to_csv(os.path.join(config.PATHS.reports_dir, "hotspot_driver_report.csv"), index=False)
    
    return hotspots
