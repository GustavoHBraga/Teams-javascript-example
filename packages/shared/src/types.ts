import { BotStatus, BotScope, DocumentStatus, MessageRole, AIModel } from './enums';

/**
 * Base entity with common fields
 */
export interface BaseEntity {
  id: string;
  createdAt: Date;
  updatedAt: Date;
}

/**
 * User information
 */
export interface User {
  id: string;
  teamsId: string;
  name: string;
  email: string;
  avatarUrl?: string;
}

/**
 * Squad/Team information
 */
export interface Squad {
  id: string;
  name: string;
  description?: string;
  members: string[]; // User IDs
  createdBy: string;
  createdAt: Date;
}

/**
 * Document uploaded for RAG
 */
export interface Document extends BaseEntity {
  botId: string;
  name: string;
  originalName: string;
  mimeType: string;
  size: number;
  storageUrl: string;
  status: DocumentStatus;
  vectorIndexId?: string;
  uploadedBy: string;
  metadata?: Record<string, any>;
}

/**
 * Bot configuration
 */
export interface BotConfig {
  model: AIModel;
  temperature: number;
  maxTokens: number;
  systemPrompt: string;
  enableRAG: boolean;
  ragTopK?: number;
  ragThreshold?: number;
}

/**
 * Bot entity
 */
export interface Bot extends BaseEntity {
  name: string;
  description: string;
  instructions: string;
  scope: BotScope;
  status: BotStatus;
  config: BotConfig;
  createdBy: string;
  squadId?: string;
  documents: string[]; // Document IDs
  tags: string[];
  avatarUrl?: string;
  conversationCount: number;
  lastUsedAt?: Date;
}

/**
 * Conversation message
 */
export interface Message extends BaseEntity {
  conversationId: string;
  role: MessageRole;
  content: string;
  userId?: string;
  metadata?: {
    sources?: DocumentSource[];
    tokens?: number;
    model?: string;
  };
}

/**
 * Document source reference for RAG
 */
export interface DocumentSource {
  documentId: string;
  documentName: string;
  snippet: string;
  score: number;
  pageNumber?: number;
}

/**
 * Conversation thread
 */
export interface Conversation extends BaseEntity {
  botId: string;
  userId: string;
  title: string;
  messages: string[]; // Message IDs
  isActive: boolean;
}

/**
 * Analytics data
 */
export interface BotAnalytics {
  botId: string;
  totalConversations: number;
  totalMessages: number;
  averageResponseTime: number;
  successRate: number;
  topQuestions: Array<{ question: string; count: number }>;
  usageByDate: Array<{ date: string; count: number }>;
}
