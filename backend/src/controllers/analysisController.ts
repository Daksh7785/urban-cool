import { Request, Response } from 'express';
import Project from '../models/Project';
import { analysisQueue } from '../services/queueService';

export const triggerAnalysis = async (req: Request, res: Response) => {
  try {
    const { name, city, bbox } = req.body;
    const userId = (req as any).user.id;
    
    const project = new Project({ userId, name, city, bbox, status: 'Queued' });
    await project.save();
    
    await analysisQueue.add('analyze', { projectId: project._id, city, bbox });
    
    res.json({ message: 'Analysis queued successfully', project });
  } catch (error) {
    res.status(500).json({ message: 'Error queueing analysis' });
  }
};
