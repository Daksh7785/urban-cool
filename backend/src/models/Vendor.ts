import mongoose from 'mongoose';

const vendorSchema = new mongoose.Schema({
  tenantId: { type: String, required: true, default: 'SYSTEM_TENANT' },
  name: { type: String, required: true },
  type: { type: String, enum: ['NGO', 'Contractor', 'CSR_Partner'], required: true },
  specialties: { type: [String], required: true }, // e.g. ['Cool Roofs', 'Tree Plantation']
  verified: { type: Boolean, default: false },
  rating: { type: Number, default: 0 },
  createdAt: { type: Date, default: Date.now }
});

export const Vendor = mongoose.model('Vendor', vendorSchema);
