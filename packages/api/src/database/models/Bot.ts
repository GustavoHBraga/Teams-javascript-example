import mongoose, { Schema, Document } from 'mongoose';
import { Bot as IBot, BotStatus, BotScope, AIModel } from '@teams-bot/shared';

export interface BotDocument extends Omit<IBot, 'id'>, Document {
  _id: string;
}

const BotConfigSchema = new Schema(
  {
    model: { type: String, enum: Object.values(AIModel), default: AIModel.GPT4_TURBO },
    temperature: { type: Number, default: 0.7, min: 0, max: 2 },
    maxTokens: { type: Number, default: 2000, min: 100, max: 8000 },
    systemPrompt: { type: String },
    enableRAG: { type: Boolean, default: true },
    ragTopK: { type: Number, default: 5, min: 1, max: 10 },
    ragThreshold: { type: Number, default: 0.7, min: 0, max: 1 },
  },
  { _id: false }
);

const BotSchema = new Schema<BotDocument>(
  {
    name: { type: String, required: true, trim: true, minlength: 3, maxlength: 100 },
    description: { type: String, required: true, trim: true, minlength: 10, maxlength: 500 },
    instructions: { type: String, required: true, trim: true, minlength: 20, maxlength: 5000 },
    scope: {
      type: String,
      enum: Object.values(BotScope),
      required: true,
      default: BotScope.PERSONAL,
    },
    status: {
      type: String,
      enum: Object.values(BotStatus),
      default: BotStatus.ACTIVE,
      index: true,
    },
    config: { type: BotConfigSchema, required: true },
    createdBy: { type: String, required: true, index: true },
    squadId: { type: String, index: true },
    documents: [{ type: String }],
    tags: [{ type: String, trim: true }],
    avatarUrl: { type: String },
    conversationCount: { type: Number, default: 0 },
    lastUsedAt: { type: Date },
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

// Indexes for better query performance
BotSchema.index({ name: 'text', description: 'text', tags: 'text' });
BotSchema.index({ createdBy: 1, scope: 1 });
BotSchema.index({ squadId: 1, scope: 1 });
BotSchema.index({ status: 1, createdAt: -1 });

export const BotModel = mongoose.model<BotDocument>('Bot', BotSchema);
