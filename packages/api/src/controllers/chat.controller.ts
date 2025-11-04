import { Request, Response } from 'express';

import { MessageRole, HTTP_STATUS, ERROR_CODES } from '@teams-bot/shared';

import { asyncHandler, sendSuccess } from '../middleware';
import { ConversationModel, MessageModel } from '../database/models';
import { botService, aiService, ragService } from '../services';
import { logger } from '../utils/logger';
import { AppError } from '../middleware/errorHandler';

/**
 * Send a message and get AI response
 */
export const sendMessage = asyncHandler(async (req: Request, res: Response) => {
  const userId = (req as any).user.id;
  const { botId, content, conversationId } = req.body;

  // Get bot details
  const bot = await botService.getBotById(botId, userId);

  // Find or create conversation
  let conversation;
  if (conversationId) {
    conversation = await ConversationModel.findById(conversationId);
    if (!conversation) {
      throw new AppError(
        HTTP_STATUS.NOT_FOUND,
        ERROR_CODES.NOT_FOUND,
        'Conversation not found'
      );
    }
  } else {
    conversation = await ConversationModel.create({
      botId,
      userId,
      title: content.substring(0, 50),
      messages: [],
      isActive: true,
    });
  }

  // Create user message
  const userMessage = await MessageModel.create({
    conversationId: conversation._id.toString(),
    role: MessageRole.USER,
    content,
    userId,
  });

  conversation.messages.push(userMessage._id.toString());
  await conversation.save();

  try {
    // Get relevant context from RAG if enabled
    let context: any[] = [];
    if (bot.config.enableRAG && bot.documents.length > 0) {
      context = await ragService.searchDocuments(
        botId,
        content,
        bot.config.ragTopK || 5
      );
    }

    // Generate AI response
    const aiResponse = await aiService.generateResponse({
      prompt: content,
      systemPrompt: bot.config.systemPrompt || bot.instructions,
      model: bot.config.model,
      temperature: bot.config.temperature,
      maxTokens: bot.config.maxTokens,
      context,
    });

    // Create assistant message
    const assistantMessage = await MessageModel.create({
      conversationId: conversation._id.toString(),
      role: MessageRole.ASSISTANT,
      content: aiResponse.content,
      metadata: {
        sources: context,
        tokens: aiResponse.usage.totalTokens,
        model: aiResponse.model,
      },
    });

    conversation.messages.push(assistantMessage._id.toString());
    await conversation.save();

    // Update bot stats
    await botService.updateBot(botId, bot.createdBy, {
      conversationCount: bot.conversationCount + 1,
      lastUsedAt: new Date(),
    } as any);

    sendSuccess(res, {
      conversation: conversation.toJSON(),
      userMessage: userMessage.toJSON(),
      assistantMessage: assistantMessage.toJSON(),
    });
  } catch (error) {
    logger.error('Error generating response:', error);
    throw error;
  }
});

/**
 * Get conversation history
 */
export const getConversation = asyncHandler(async (req: Request, res: Response) => {
  const { conversationId } = req.params;
  const userId = (req as any).user.id;

  const conversation = await ConversationModel.findById(conversationId);

  if (!conversation) {
    throw new AppError(
      HTTP_STATUS.NOT_FOUND,
      ERROR_CODES.NOT_FOUND,
      'Conversation not found'
    );
  }

  // Check permission
  if (conversation.userId !== userId) {
    throw new AppError(
      HTTP_STATUS.FORBIDDEN,
      ERROR_CODES.FORBIDDEN,
      'You do not have permission to access this conversation'
    );
  }

  // Get all messages
  const messages = await MessageModel.find({
    _id: { $in: conversation.messages },
  }).sort({ createdAt: 1 });

  sendSuccess(res, {
    conversation: conversation.toJSON(),
    messages: messages.map((m) => m.toJSON()),
  });
});

/**
 * List user's conversations
 */
export const listConversations = asyncHandler(async (req: Request, res: Response) => {
  const userId = (req as any).user.id;
  const { botId } = req.query;

  const filter: any = { userId, isActive: true };
  if (botId) filter.botId = botId;

  const conversations = await ConversationModel.find(filter)
    .sort({ updatedAt: -1 })
    .limit(50);

  sendSuccess(res, conversations.map((c) => c.toJSON()));
});

/**
 * Delete conversation
 */
export const deleteConversation = asyncHandler(async (req: Request, res: Response) => {
  const { conversationId } = req.params;
  const userId = (req as any).user.id;

  const conversation = await ConversationModel.findById(conversationId);

  if (!conversation) {
    throw new AppError(
      HTTP_STATUS.NOT_FOUND,
      ERROR_CODES.NOT_FOUND,
      'Conversation not found'
    );
  }

  if (conversation.userId !== userId) {
    throw new AppError(
      HTTP_STATUS.FORBIDDEN,
      ERROR_CODES.FORBIDDEN,
      'You do not have permission to delete this conversation'
    );
  }

  conversation.isActive = false;
  await conversation.save();

  sendSuccess(res, { message: 'Conversation deleted' }, HTTP_STATUS.NO_CONTENT);
});
