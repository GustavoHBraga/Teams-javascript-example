import mongoose, { Schema, Document } from 'mongoose';
import { Document as IDocument, DocumentStatus } from '@teams-bot/shared';

export interface DocumentDocument extends Omit<IDocument, 'id'>, Document {
  _id: string;
}

const DocumentSchema = new Schema<DocumentDocument>(
  {
    botId: { type: String, required: true, index: true },
    name: { type: String, required: true, trim: true },
    originalName: { type: String, required: true },
    mimeType: { type: String, required: true },
    size: { type: Number, required: true },
    storageUrl: { type: String, required: true },
    status: {
      type: String,
      enum: Object.values(DocumentStatus),
      default: DocumentStatus.PENDING,
      index: true,
    },
    vectorIndexId: { type: String },
    uploadedBy: { type: String, required: true, index: true },
    metadata: { type: Schema.Types.Mixed },
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
DocumentSchema.index({ botId: 1, status: 1 });
DocumentSchema.index({ uploadedBy: 1, createdAt: -1 });

export const DocumentModel = mongoose.model<DocumentDocument>('Document', DocumentSchema);
