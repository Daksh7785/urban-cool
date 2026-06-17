import mongoose, { Document, Schema } from 'mongoose';

export interface IProject extends Document {
  userId: mongoose.Types.ObjectId;
  name: string;
  city: string;
  bbox: string;
  status: string;
}

const projectSchema: Schema = new Schema({
  userId: { type: Schema.Types.ObjectId, ref: 'User', required: true },
  name: { type: String, required: true },
  city: { type: String, required: true },
  bbox: { type: String, required: true },
  status: { type: String, default: 'Pending' }
}, { timestamps: true });

export default mongoose.model<IProject>('Project', projectSchema);
