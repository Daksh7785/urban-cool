import { Queue, Worker } from 'bullmq';
import Redis from 'ioredis';
import axios from 'axios';
import Project from '../models/Project';

const connection = new Redis(process.env.REDIS_HOST ? `redis://${process.env.REDIS_HOST}:${process.env.REDIS_PORT}` : 'redis://localhost:6379');

export const analysisQueue = new Queue('analysisQueue', { connection });

const worker = new Worker('analysisQueue', async job => {
  const { projectId, city, bbox } = job.data;
  console.log(`Processing analysis for project ${projectId}`);
  
  // Call Analytics FastAPI Service
  try {
    const response = await axios.post(`${process.env.ANALYTICS_URL}/analyze`, {
      projectId, city, bbox
    });
    
    // Update project status
    await Project.findByIdAndUpdate(projectId, { status: 'Completed' });
    
    return response.data;
  } catch (error) {
    await Project.findByIdAndUpdate(projectId, { status: 'Failed' });
    console.error('Analysis failed', error);
    throw error;
  }
}, { connection });

worker.on('completed', job => {
  console.log(`${job.id} has completed!`);
});

worker.on('failed', (job, err) => {
  console.log(`${job?.id} has failed with ${err.message}`);
});
