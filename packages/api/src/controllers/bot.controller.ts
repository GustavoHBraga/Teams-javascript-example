import { Request, Response } from 'express';

import { createBotSchema, updateBotSchema, HTTP_STATUS } from '@teams-bot/shared';

import { botService } from '../services';
import { asyncHandler, sendSuccess } from '../middleware';

/**
 * Create a new bot
 */
export const createBot = asyncHandler(async (req: Request, res: Response) => {
  const userId = (req as any).user.id;
  const input = createBotSchema.parse(req.body);

  const bot = await botService.createBot(userId, input);

  sendSuccess(res, bot, HTTP_STATUS.CREATED);
});

/**
 * Get bot by ID
 */
export const getBotById = asyncHandler(async (req: Request, res: Response) => {
  const { botId } = req.params;
  const userId = (req as any).user?.id;

  const bot = await botService.getBotById(botId, userId);

  sendSuccess(res, bot);
});

/**
 * List bots
 */
export const listBots = asyncHandler(async (req: Request, res: Response) => {
  const userId = (req as any).user.id;
  const query = req.query;

  const result = await botService.listBots(userId, query as any);

  sendSuccess(res, result);
});

/**
 * Update bot
 */
export const updateBot = asyncHandler(async (req: Request, res: Response) => {
  const { botId } = req.params;
  const userId = (req as any).user.id;
  const input = updateBotSchema.parse(req.body);

  const bot = await botService.updateBot(botId, userId, input);

  sendSuccess(res, bot);
});

/**
 * Delete bot
 */
export const deleteBot = asyncHandler(async (req: Request, res: Response) => {
  const { botId } = req.params;
  const userId = (req as any).user.id;

  await botService.deleteBot(botId, userId);

  sendSuccess(res, { message: 'Bot deleted successfully' }, HTTP_STATUS.NO_CONTENT);
});
