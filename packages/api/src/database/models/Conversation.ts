import mongoose, { Schema, Document } from 'mongoose';
import { Conversation as IConversation } from '@teams-bot/shared';

export interface ConversationDocument extends Omit<IConversation, 'id'>, Document {
  _id: string;
}

const ConversationSchema = new Schema<ConversationDocument>(
  {
    botId: { type: String, required: true, index: true },
    userId: { type: String, required: true, index: true },
    title: { type: String, required: true, default: 'New Conversation' },
    messages: [{ type: String }],
    isActive: { type: Boolean, default: true, index: true },
  },
  {
    timestamps: true,
    toJSON: {
      transform: (_doc: any, ret: any) => {
        ret.id = ret._id.toString();
        delete ret._id;
        delete ret.__v;
        return ret;
      },
    },
  }
);

// Indexes
ConversationSchema.index({ botId: 1, userId: 1, isActive: 1 });
ConversationSchema.index({ userId: 1, updatedAt: -1 });

export const ConversationModel = mongoose.model<ConversationDocument>(
  'Conversation',
  ConversationSchema
);
