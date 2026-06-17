import mongoose from 'mongoose';

const hotspotSchema = new mongoose.Schema({
  tenantId: { type: String, required: true, default: 'SYSTEM_TENANT' },
  projectId: { type: mongoose.Schema.Types.ObjectId, ref: 'Project', required: true },
  hotspot_id: { type: String, required: true },
  mean_lst: { type: Number, required: true },
  severity: { type: Number, required: true },
  geometry: { type: Object, required: true }, // GeoJSON Polygon
  top_drivers: { type: Array, required: true },
  forecast: { type: Object },
  digital_twin_timeline: { type: Object },
  uhvi_score: { type: Object },
  pareto_optimization: { type: Object },
  createdAt: { type: Date, default: Date.now }
});

export const Hotspot = mongoose.model('Hotspot', hotspotSchema);
