import { Router } from 'express';

import botsRoutes from './bots.routes';
import chatRoutes from './chat.routes';
import documentsRoutes from './documents.routes';

const router = Router();

// Health check
router.get('/health', (_req, res) => {
  res.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    service: 'teams-bot-automation-api',
  });
});

// API routes
router.use('/bots', botsRoutes);
router.use('/bots', documentsRoutes); // Rotas de documentos também começam com /bots
router.use('/chat', chatRoutes);

export default router;
