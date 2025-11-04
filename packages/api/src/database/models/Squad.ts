import mongoose, { Schema, Document } from 'mongoose';
import { Squad as ISquad } from '@teams-bot/shared';

export interface SquadDocument extends Omit<ISquad, 'id'>, Document {
  _id: string;
}

const SquadSchema = new Schema<SquadDocument>(
  {
    name: { type: String, required: true, trim: true, minlength: 3, maxlength: 100 },
    description: { type: String, trim: true, maxlength: 500 },
    members: [{ type: String, required: true }],
    createdBy: { type: String, required: true, index: true },
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
SquadSchema.index({ name: 'text', description: 'text' });
SquadSchema.index({ members: 1 });
SquadSchema.index({ createdBy: 1, createdAt: -1 });

export const SquadModel = mongoose.model<SquadDocument>('Squad', SquadSchema);
