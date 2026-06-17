import express from 'express';
import mongoose from 'mongoose';
import cors from 'cors';
import helmet from 'helmet';
import rateLimit from 'express-rate-limit';
import dotenv from 'dotenv';
import { createServer } from 'http';
import { Server } from 'socket.io';

dotenv.config();

import authRoutes from './routes/authRoutes';
import analysisRoutes from './routes/analysisRoutes';
import copilotRoutes from './routes/copilotRoutes';

const app = express();
const httpServer = createServer(app);
const io = new Server(httpServer, {
  cors: { origin: '*' }
});

// Phase 15: Enterprise Security
app.use(helmet());
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // limit each IP to 100 requests per windowMs
});
app.use(limiter);

app.use(cors());
app.use(express.json());

// Routes
app.use('/api/auth', authRoutes);
app.use('/api/analysis', analysisRoutes);
app.use('/api/copilot', copilotRoutes);

// Socket.io for Real-time Digital Twin Telemetry
io.on('connection', (socket) => {
  console.log('Client connected for telemetry');
});

const PORT = process.env.PORT || 5000;

mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/urbanos')
  .then(() => {
    httpServer.listen(PORT, () => {
      console.log(`UrbanOS Global API running on port ${PORT}`);
    });
  })
  .catch((err) => {
    console.error('Database connection failed', err);
  });
