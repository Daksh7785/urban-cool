
import logging
import numpy as np
import config
from sklearn.cluster import DBSCAN

logger = logging.getLogger(__name__)

def detect_hotspots(gdf_grid):
    logger.info("Detecting hotspots...")
    
    lst = gdf_grid['lst'].values
    mean_lst = np.mean(lst)
    anomaly = lst - mean_lst
    gdf_grid['lst_anomaly'] = anomaly
    
    threshold = np.percentile(anomaly, config.HOTSPOT_PERCENTILE)
    hot_mask = anomaly >= threshold
    
    hot_indices = np.where(hot_mask)[0]
    
    if len(hot_indices) == 0:
        logger.warning("No hotspots detected!")
        return []
        
    hot_coords = np.column_stack((gdf_grid.geometry.centroid.x.iloc[hot_indices], 
                                  gdf_grid.geometry.centroid.y.iloc[hot_indices]))
    
    db = DBSCAN(eps=2000, min_samples=3).fit(hot_coords)
    labels = db.labels_
    
    hotspots = []
    unique_labels = set(labels)
    for label in unique_labels:
        if label == -1:
            continue
        cluster_idx = hot_indices[labels == label]
        hotspots.append({
            'hotspot_id': int(label),
            'cell_indices': cluster_idx.tolist(),
            'mean_lst': float(np.mean(lst[cluster_idx])),
            'severity': float(np.mean(anomaly[cluster_idx]) * len(cluster_idx))
        })
    
    hotspots = sorted(hotspots, key=lambda x: x['severity'], reverse=True)[:20]
    
    # If DBSCAN found no clusters but we have hot cells, just make the top cell a hotspot
    if not hotspots and len(hot_indices) > 0:
        top_idx = hot_indices[np.argmax(anomaly[hot_indices])]
        hotspots.append({
            'hotspot_id': 0,
            'cell_indices': [int(top_idx)],
            'mean_lst': float(lst[top_idx]),
            'severity': float(anomaly[top_idx])
        })
        
    return hotspots
