import mongoose from 'mongoose';

const jobSchema = new mongoose.Schema({
  tenantId: { type: String, required: true, default: 'SYSTEM_TENANT' },
  projectId: { type: mongoose.Schema.Types.ObjectId, ref: 'Project', required: true },
  status: { type: String, enum: ['queued', 'running', 'completed', 'failed'], default: 'queued' },
  type: { type: String, required: true },
  result: { type: Object },
  createdAt: { type: Date, default: Date.now },
  updatedAt: { type: Date, default: Date.now }
});

export const Job = mongoose.model('Job', jobSchema);
