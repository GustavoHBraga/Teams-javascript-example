import { Router } from 'express';

import * as botController from '../controllers/bot.controller';
import { authenticate } from '../middleware';
import { validateBody } from '../middleware/validate';
import { createBotSchema, updateBotSchema } from '@teams-bot/shared';

const router = Router();

// All bot routes require authentication
router.use(authenticate);

// Create a new bot
router.post('/', validateBody(createBotSchema), botController.createBot);

// List bots
router.get('/', botController.listBots);

// Get bot by ID
router.get('/:botId', botController.getBotById);

// Update bot
router.patch('/:botId', validateBody(updateBotSchema), botController.updateBot);

// Delete bot
router.delete('/:botId', botController.deleteBot);

export default router;
