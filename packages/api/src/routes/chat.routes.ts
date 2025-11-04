import { Router } from 'express';

import * as chatController from '../controllers/chat.controller';
import { authenticate } from '../middleware';
import { validateBody } from '../middleware/validate';
import { sendMessageSchema } from '@teams-bot/shared';

const router = Router();

// All chat routes require authentication
router.use(authenticate);

// Send a message
router.post('/messages', validateBody(sendMessageSchema), chatController.sendMessage);

// Get conversation
router.get('/conversations/:conversationId', chatController.getConversation);

// List conversations
router.get('/conversations', chatController.listConversations);

// Delete conversation
router.delete('/conversations/:conversationId', chatController.deleteConversation);

export default router;
