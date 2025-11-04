import { api } from './api';
import type { Bot, CreateBotInput, ListBotsQuery, PaginatedResponse } from '@teams-bot/shared';

export const botApi = {
  // Get all bots
  async list(query?: ListBotsQuery): Promise<PaginatedResponse<Bot>> {
    const { data } = await api.get('/bots', { params: query });
    return data.data;
  },

  // Get bot by ID
  async getById(id: string): Promise<Bot> {
    const { data } = await api.get(`/bots/${id}`);
    return data.data;
  },

  // Create new bot
  async create(input: CreateBotInput): Promise<Bot> {
    const { data } = await api.post('/bots', input);
    return data.data;
  },

  // Update bot
  async update(id: string, input: Partial<CreateBotInput>): Promise<Bot> {
    const { data } = await api.patch(`/bots/${id}`, input);
    return data.data;
  },

  // Delete bot
  async delete(id: string): Promise<void> {
    await api.delete(`/bots/${id}`);
  },
};

export const chatApi = {
  // Send message
  async sendMessage(botId: string, content: string, conversationId?: string) {
    const { data } = await api.post('/chat/messages', {
      botId,
      content,
      conversationId,
      userId: 'test-user-123',
    });
    return data.data;
  },

  // Get conversations
  async getConversations(botId?: string) {
    const { data } = await api.get('/chat/conversations', {
      params: botId ? { botId } : {},
    });
    return data.data;
  },

  // Get conversation by ID
  async getConversation(id: string) {
    const { data } = await api.get(`/chat/conversations/${id}`);
    return data.data;
  },
};
