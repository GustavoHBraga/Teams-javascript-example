import { z } from 'zod';

import { BotStatus, BotScope, AIModel } from './enums';

/**
 * Validation schema for creating a bot
 */
export const createBotSchema = z.object({
  name: z.string().min(3).max(100),
  description: z.string().min(10).max(500),
  instructions: z.string().min(20).max(5000),
  scope: z.nativeEnum(BotScope),
  squadId: z.string().optional(),
  config: z.object({
    model: z.nativeEnum(AIModel).default(AIModel.GPT4_TURBO),
    temperature: z.number().min(0).max(2).default(0.7),
    maxTokens: z.number().min(100).max(8000).default(2000),
    systemPrompt: z.string().optional(),
    enableRAG: z.boolean().default(true),
    ragTopK: z.number().min(1).max(10).optional(),
    ragThreshold: z.number().min(0).max(1).optional(),
  }),
  tags: z.array(z.string()).default([]),
});

/**
 * Validation schema for updating a bot
 */
export const updateBotSchema = createBotSchema.partial();

/**
 * Validation schema for uploading documents
 */
export const uploadDocumentSchema = z.object({
  botId: z.string().uuid(),
  file: z.any(), // File validation happens at multipart level
  metadata: z.record(z.any()).optional(),
});

/**
 * Validation schema for sending a message
 */
export const sendMessageSchema = z.object({
  conversationId: z.string().uuid().optional(),
  botId: z.string().uuid(),
  content: z.string().min(1).max(4000),
  userId: z.string(),
});

/**
 * Validation schema for creating a squad
 */
export const createSquadSchema = z.object({
  name: z.string().min(3).max(100),
  description: z.string().max(500).optional(),
  members: z.array(z.string()).min(1),
});

/**
 * API Response wrapper
 */
export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
    details?: any;
  };
  metadata?: {
    timestamp: string;
    requestId: string;
  };
}

/**
 * Paginated response
 */
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  pageSize: number;
  totalPages: number;
}

/**
 * Query parameters for listing bots
 */
export interface ListBotsQuery {
  page?: number;
  pageSize?: number;
  scope?: BotScope;
  status?: BotStatus;
  search?: string;
  tags?: string[];
  squadId?: string;
  createdBy?: string;
  sortBy?: 'createdAt' | 'name' | 'lastUsedAt' | 'conversationCount';
  sortOrder?: 'asc' | 'desc';
}

export type CreateBotInput = z.infer<typeof createBotSchema>;
export type UpdateBotInput = z.infer<typeof updateBotSchema>;
export type SendMessageInput = z.infer<typeof sendMessageSchema>;
export type CreateSquadInput = z.infer<typeof createSquadSchema>;
