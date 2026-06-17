import mongoose from 'mongoose';

const projectSchema = new mongoose.Schema({
  tenantId: { type: String, required: true, default: 'SYSTEM_TENANT' },
  name: { type: String, required: true },
  city: { type: String, required: true },
  bounds: { type: Object, required: true }, // GeoJSON Polygon
  createdAt: { type: Date, default: Date.now }
});

export const Project = mongoose.model('Project', projectSchema);
