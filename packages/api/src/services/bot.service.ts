import {
  Bot,
  CreateBotInput,
  UpdateBotInput,
  ListBotsQuery,
  PaginatedResponse,
  BotStatus,
  ERROR_CODES,
  HTTP_STATUS,
  PAGINATION,
} from '@teams-bot/shared';

import { BotModel } from '../database/models';
import { AppError } from '../middleware/errorHandler';
import { logger } from '../utils/logger';

export class BotService {
  /**
   * Create a new bot
   */
  async createBot(userId: string, input: CreateBotInput): Promise<Bot> {
    try {
      logger.info('Creating new bot', { userId, name: input.name });

      const bot = await BotModel.create({
        ...input,
        createdBy: userId,
        status: BotStatus.ACTIVE,
        documents: [],
        conversationCount: 0,
      });

      return bot.toJSON() as Bot;
    } catch (error: any) {
      logger.error('Error creating bot:', error);
      throw new AppError(
        HTTP_STATUS.INTERNAL_SERVER_ERROR,
        ERROR_CODES.BOT_CREATION_FAILED,
        'Failed to create bot',
        error.message
      );
    }
  }

  /**
   * Get bot by ID
   */
  async getBotById(botId: string, userId?: string): Promise<Bot> {
    try {
      const bot = await BotModel.findById(botId);

      if (!bot) {
        throw new AppError(
          HTTP_STATUS.NOT_FOUND,
          ERROR_CODES.BOT_NOT_FOUND,
          'Bot not found'
        );
      }

      // Check permissions (simplified - in production, check squad membership)
      if (userId && bot.scope === 'personal' && bot.createdBy !== userId) {
        throw new AppError(
          HTTP_STATUS.FORBIDDEN,
          ERROR_CODES.FORBIDDEN,
          'You do not have permission to access this bot'
        );
      }

      return bot.toJSON() as Bot;
    } catch (error: any) {
      if (error instanceof AppError) throw error;

      logger.error('Error getting bot:', error);
      throw new AppError(
        HTTP_STATUS.INTERNAL_SERVER_ERROR,
        ERROR_CODES.INTERNAL_ERROR,
        'Failed to get bot',
        error.message
      );
    }
  }

  /**
   * List bots with filtering and pagination
   */
  async listBots(userId: string, query: ListBotsQuery): Promise<PaginatedResponse<Bot>> {
    try {
      const {
        page = PAGINATION.DEFAULT_PAGE,
        pageSize = PAGINATION.DEFAULT_PAGE_SIZE,
        scope,
        status,
        search,
        tags,
        squadId,
        createdBy,
        sortBy = 'createdAt',
        sortOrder = 'desc',
      } = query;

      // Build filter
      const filter: any = {};

      // Scope filter
      if (scope) {
        filter.scope = scope;
      } else {
        // Default: show user's personal bots and squad bots they have access to
        filter.$or = [
          { createdBy: userId, scope: 'personal' },
          { scope: 'squad' }, // In production, filter by squad membership
          { scope: 'organization' },
        ];
      }

      if (status) filter.status = status;
      if (squadId) filter.squadId = squadId;
      if (createdBy) filter.createdBy = createdBy;
      if (tags && tags.length > 0) filter.tags = { $in: tags };

      // Text search
      if (search) {
        filter.$text = { $search: search };
      }

      // Pagination
      const skip = (page - 1) * Math.min(pageSize, PAGINATION.MAX_PAGE_SIZE);
      const limit = Math.min(pageSize, PAGINATION.MAX_PAGE_SIZE);

      // Execute query
      const [items, total] = await Promise.all([
        BotModel.find(filter)
          .sort({ [sortBy]: sortOrder === 'asc' ? 1 : -1 })
          .skip(skip)
          .limit(limit)
          .lean(),
        BotModel.countDocuments(filter),
      ]);

      return {
        items: items.map((item) => ({
          ...item,
          id: item._id.toString(),
        })) as Bot[],
        total,
        page,
        pageSize: limit,
        totalPages: Math.ceil(total / limit),
      };
    } catch (error: any) {
      logger.error('Error listing bots:', error);
      throw new AppError(
        HTTP_STATUS.INTERNAL_SERVER_ERROR,
        ERROR_CODES.INTERNAL_ERROR,
        'Failed to list bots',
        error.message
      );
    }
  }

  /**
   * Update a bot
   */
  async updateBot(botId: string, userId: string, input: UpdateBotInput): Promise<Bot> {
    try {
      const bot = await BotModel.findById(botId);

      if (!bot) {
        throw new AppError(
          HTTP_STATUS.NOT_FOUND,
          ERROR_CODES.BOT_NOT_FOUND,
          'Bot not found'
        );
      }

      // Check permissions
      if (bot.createdBy !== userId) {
        throw new AppError(
          HTTP_STATUS.FORBIDDEN,
          ERROR_CODES.FORBIDDEN,
          'You do not have permission to update this bot'
        );
      }

      // Update fields
      Object.assign(bot, input);
      await bot.save();

      return bot.toJSON() as Bot;
    } catch (error: any) {
      if (error instanceof AppError) throw error;

      logger.error('Error updating bot:', error);
      throw new AppError(
        HTTP_STATUS.INTERNAL_SERVER_ERROR,
        ERROR_CODES.BOT_UPDATE_FAILED,
        'Failed to update bot',
        error.message
      );
    }
  }

  /**
   * Delete a bot
   */
  async deleteBot(botId: string, userId: string): Promise<void> {
    try {
      const bot = await BotModel.findById(botId);

      if (!bot) {
        throw new AppError(
          HTTP_STATUS.NOT_FOUND,
          ERROR_CODES.BOT_NOT_FOUND,
          'Bot not found'
        );
      }

      // Check permissions
      if (bot.createdBy !== userId) {
        throw new AppError(
          HTTP_STATUS.FORBIDDEN,
          ERROR_CODES.FORBIDDEN,
          'You do not have permission to delete this bot'
        );
      }

      await bot.deleteOne();

      logger.info('Bot deleted', { botId, userId });
    } catch (error: any) {
      if (error instanceof AppError) throw error;

      logger.error('Error deleting bot:', error);
      throw new AppError(
        HTTP_STATUS.INTERNAL_SERVER_ERROR,
        ERROR_CODES.BOT_DELETE_FAILED,
        'Failed to delete bot',
        error.message
      );
    }
  }
}

export const botService = new BotService();
