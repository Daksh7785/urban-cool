
import logging
import numpy as np
import pickle
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
import config
import os
import json

logger = logging.getLogger(__name__)

def train_feature_model(gdf_grid):
    logger.info("Training XGBoost feature model...")
    features = ['ndvi', 'ndbi', 'ndwi', 'albedo', 'building_density', 'building_height', 'road_density', 'population_density', 'elevation']
    X = gdf_grid[features].values
    y = gdf_grid['lst'].values
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=config.RANDOM_SEED)
    
    model = xgb.XGBRegressor(n_estimators=100, max_depth=5, random_state=config.RANDOM_SEED)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    
    if r2 < 0.3:
        logger.warning(f"Model R2 is very low ({r2:.2f}) - synthetic correlations may be weak.")
    else:
        logger.info(f"Model trained successfully. R2={r2:.2f}, RMSE={rmse:.2f}")
        
    # Save model
    with open(config.MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
        
    # Save metrics
    metrics = {"r2": r2, "rmse": rmse}
    with open(os.path.join(config.PATHS.reports_dir, "model_metrics.json"), "w") as f:
        json.dump(metrics, f)
        
    return model, features
