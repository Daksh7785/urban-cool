import mongoose, { Document, Schema } from 'mongoose';

export interface IHotspot extends Document {
  projectId: mongoose.Types.ObjectId;
  hotspot_id: number;
  mean_lst: number;
  centroid_lat: number;
  centroid_lon: number;
  affected_population: number;
  top_drivers: any[];
}

const hotspotSchema: Schema = new Schema({
  projectId: { type: Schema.Types.ObjectId, ref: 'Project', required: true },
  hotspot_id: { type: Number, required: true },
  mean_lst: { type: Number, required: true },
  centroid_lat: { type: Number, required: true },
  centroid_lon: { type: Number, required: true },
  affected_population: { type: Number, required: true },
  top_drivers: { type: Array, default: [] }
}, { timestamps: true });

export default mongoose.model<IHotspot>('Hotspot', hotspotSchema);
