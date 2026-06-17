import mongoose, { Document, Schema } from 'mongoose';

export interface IUser extends Document {
  email: string;
  passwordHash: string;
  role: string;
  name: string;
}

const userSchema: Schema = new Schema({
  email: { type: String, required: true, unique: true },
  passwordHash: { type: String, required: true },
  role: { type: String, enum: ['Admin', 'Researcher', 'Judge', 'Viewer'], default: 'Viewer' },
  name: { type: String, required: true }
}, { timestamps: true });

export default mongoose.model<IUser>('User', userSchema);
