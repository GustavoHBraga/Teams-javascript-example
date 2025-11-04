import { OpenAI } from 'openai';

import { AIModel, DocumentSource, ERROR_CODES, HTTP_STATUS } from '@teams-bot/shared';

import { config } from '../config';
import { logger } from '../utils/logger';
import { AppError } from '../middleware/errorHandler';

export interface GenerateResponseOptions {
  prompt: string;
  systemPrompt?: string;
  model?: AIModel;
  temperature?: number;
  maxTokens?: number;
  context?: DocumentSource[];
}

export interface GenerateResponseResult {
  content: string;
  usage: {
    promptTokens: number;
    completionTokens: number;
    totalTokens: number;
  };
  model: string;
}

export class AIService {
  private readonly client: OpenAI;

  constructor() {
    // Initialize OpenAI client (works for both Azure OpenAI and OpenAI)
    if (config.openai.azureApiKey && config.openai.azureEndpoint) {
      // Azure OpenAI
      this.client = new OpenAI({
        apiKey: config.openai.azureApiKey,
        baseURL: `${config.openai.azureEndpoint}/openai/deployments/${config.openai.azureDeploymentName}`,
        defaultQuery: { 'api-version': config.openai.azureApiVersion },
        defaultHeaders: { 'api-key': config.openai.azureApiKey },
      });
    } else if (config.openai.apiKey) {
      // Regular OpenAI
      this.client = new OpenAI({
        apiKey: config.openai.apiKey,
      });
    } else {
      logger.warn('No OpenAI API key configured. AI features will not work.');
      // Create a dummy client to avoid undefined
      this.client = new OpenAI({
        apiKey: 'dummy-key',
      });
    }
  }

  /**
   * Generate a response using the configured AI model
   */
  async generateResponse(options: GenerateResponseOptions): Promise<GenerateResponseResult> {
    try {
      const {
        prompt,
        systemPrompt = 'You are a helpful assistant.',
        model = AIModel.GPT4_TURBO,
        temperature = 0.7,
        maxTokens = 2000,
        context = [],
      } = options;

      // Build messages array
      const messages: any[] = [
        {
          role: 'system',
          content: systemPrompt,
        },
      ];

      // Add context from RAG if available
      if (context.length > 0) {
        const contextText = context
          .map(
            (doc, i) =>
              `[Document ${i + 1}: ${doc.documentName}]\n${doc.snippet}\n(Relevance: ${(doc.score * 100).toFixed(1)}%)`
          )
          .join('\n\n');

        messages.push({
          role: 'system',
          content: `Here is relevant context from the knowledge base:\n\n${contextText}`,
        });
      }

      messages.push({
        role: 'user',
        content: prompt,
      });

      logger.info('Generating AI response', {
        model,
        temperature,
        maxTokens,
        hasContext: context.length > 0,
      });

      const response = await this.client.chat.completions.create({
        model,
        messages,
        temperature,
        max_tokens: maxTokens,
      });

      const choice = response.choices[0];
      if (!choice?.message) {
        throw new AppError(
          HTTP_STATUS.INTERNAL_SERVER_ERROR,
          ERROR_CODES.AI_SERVICE_ERROR,
          'No response from AI model'
        );
      }

      return {
        content: choice.message.content || '',
        usage: {
          promptTokens: response.usage?.prompt_tokens || 0,
          completionTokens: response.usage?.completion_tokens || 0,
          totalTokens: response.usage?.total_tokens || 0,
        },
        model: response.model,
      };
    } catch (error: any) {
      logger.error('Error generating AI response:', error);

      if (error instanceof AppError) {
        throw error;
      }

      throw new AppError(
        HTTP_STATUS.INTERNAL_SERVER_ERROR,
        ERROR_CODES.AI_SERVICE_ERROR,
        'Failed to generate AI response',
        error.message
      );
    }
  }

  /**
   * Generate embeddings for text (used for RAG)
   */
  async generateEmbeddings(text: string): Promise<number[]> {
    try {
      const response = await this.client.embeddings.create({
        model: 'text-embedding-ada-002',
        input: text,
      });

      return response.data[0].embedding;
    } catch (error: any) {
      logger.error('Error generating embeddings:', error);
      throw new AppError(
        HTTP_STATUS.INTERNAL_SERVER_ERROR,
        ERROR_CODES.AI_SERVICE_ERROR,
        'Failed to generate embeddings',
        error.message
      );
    }
  }
}

export const aiService = new AIService();
