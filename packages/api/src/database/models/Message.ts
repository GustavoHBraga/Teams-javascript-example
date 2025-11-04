import mongoose, { Schema, Document } from 'mongoose';
import { Message as IMessage, MessageRole } from '@teams-bot/shared';

export interface MessageDocument extends Omit<IMessage, 'id'>, Document {
  _id: string;
}

const DocumentSourceSchema = new Schema(
  {
    documentId: { type: String, required: true },
    documentName: { type: String, required: true },
    snippet: { type: String, required: true },
    score: { type: Number, required: true },
    pageNumber: { type: Number },
  },
  { _id: false }
);

const MessageSchema = new Schema<MessageDocument>(
  {
    conversationId: { type: String, required: true, index: true },
    role: {
      type: String,
      enum: Object.values(MessageRole),
      required: true,
    },
    content: { type: String, required: true },
    userId: { type: String, index: true },
    metadata: {
      sources: [DocumentSourceSchema],
      tokens: { type: Number },
      model: { type: String },
    },
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
MessageSchema.index({ conversationId: 1, createdAt: 1 });
MessageSchema.index({ userId: 1, createdAt: -1 });

export const MessageModel = mongoose.model<MessageDocument>('Message', MessageSchema);
