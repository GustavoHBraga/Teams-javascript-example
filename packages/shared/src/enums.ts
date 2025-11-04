/**
 * Bot status types
 */
export enum BotStatus {
  ACTIVE = 'active',
  INACTIVE = 'inactive',
  TRAINING = 'training',
  ERROR = 'error',
}

/**
 * Bot visibility scope
 */
export enum BotScope {
  PERSONAL = 'personal',
  SQUAD = 'squad',
  ORGANIZATION = 'organization',
}

/**
 * Document processing status
 */
export enum DocumentStatus {
  PENDING = 'pending',
  PROCESSING = 'processing',
  COMPLETED = 'completed',
  FAILED = 'failed',
}

/**
 * Message role types
 */
export enum MessageRole {
  USER = 'user',
  ASSISTANT = 'assistant',
  SYSTEM = 'system',
}

/**
 * AI Model types
 */
export enum AIModel {
  GPT4 = 'gpt-4',
  GPT4_TURBO = 'gpt-4-turbo',
  GPT35_TURBO = 'gpt-3.5-turbo',
}
