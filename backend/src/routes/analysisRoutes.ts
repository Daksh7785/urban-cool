import express from 'express';
import { triggerAnalysis } from '../controllers/analysisController';
import { auth } from '../middleware/auth';

const router = express.Router();

router.post('/run', auth, triggerAnalysis);

export default router;
