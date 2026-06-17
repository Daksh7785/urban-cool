import express from 'express';
import { chatWithCopilot } from '../controllers/copilotController';

const router = express.Router();

router.post('/chat', chatWithCopilot);

export default router;
