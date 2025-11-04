import { Request, Response } from 'express';
import { Document } from '../database/models';
import { BotModel } from '../database/models/Bot';
import { ragService } from '../services';
import { AppError } from '../middleware/errorHandler';
import { logger } from '../utils/logger';

/**
 * Upload de documento para um bot
 */
export async function uploadDocument(req: Request, res: Response): Promise<void> {
  const { botId } = req.params;
  const { title, description } = req.body;
  const file = req.file;
  const userId = (req as any).user?.userId;

  if (!file) {
    throw new AppError('BAD_REQUEST', 'Nenhum arquivo foi enviado', 400);
  }

  // Verificar se o bot existe e pertence ao usuário
  const bot = await BotModel.findById(botId);
  if (!bot) {
    throw new AppError('NOT_FOUND', 'Bot não encontrado', 404);
  }

  if (bot.createdBy !== userId && bot.scope !== 'organization') {
    throw new AppError('FORBIDDEN', 'Você não tem permissão para adicionar documentos a este bot', 403);
  }

  // Criar documento no banco
  const document = await Document.create({
    botId,
    title: title || file.originalname,
    description,
    filename: file.originalname,
    mimeType: file.mimetype,
    size: file.size,
    status: 'processing',
    uploadedBy: userId,
  });

  // Processar documento de forma assíncrona (em produção, usar fila)
  processDocumentAsync(document.id, file.buffer, bot.id)
    .then(() => {
      logger.info(`Documento ${document.id} processado com sucesso`);
    })
    .catch((error) => {
      logger.error(`Erro ao processar documento ${document.id}:`, error);
    });

  res.status(201).json({
    success: true,
    message: 'Documento enviado e em processamento',
    data: document,
  });
}

/**
 * Processar documento de forma assíncrona
 */
async function processDocumentAsync(documentId: string, buffer: Buffer, botId: string): Promise<void> {
  try {
    const document = await Document.findById(documentId);
    if (!document) {
      throw new Error('Documento não encontrado');
    }

    // Extrair texto do documento
    const content = buffer.toString('utf-8'); // Simplificado - em produção usar bibliotecas específicas

    // Processar com RAG service (gerar embeddings e indexar)
    await ragService.processDocument(botId, {
      id: documentId,
      content,
      metadata: {
        title: document.title,
        filename: document.filename,
        mimeType: document.mimeType,
      },
    });

    // Atualizar status do documento
    document.status = 'completed';
    document.processedAt = new Date();
    document.content = content;
    document.metadata = {
      wordCount: content.split(/\s+/).length,
      charCount: content.length,
    };
    await document.save();

    logger.info(`Documento ${documentId} processado com sucesso`);
  } catch (error) {
    logger.error(`Erro ao processar documento ${documentId}:`, error);

    // Atualizar status para erro
    const document = await Document.findById(documentId);
    if (document) {
      document.status = 'failed';
      document.metadata = {
        error: error instanceof Error ? error.message : 'Erro desconhecido',
      };
      await document.save();
    }

    throw error;
  }
}

/**
 * Listar documentos de um bot
 */
export async function getDocuments(req: Request, res: Response): Promise<void> {
  const { botId } = req.params;
  const userId = (req as any).user?.userId;

  // Verificar se o bot existe e o usuário tem acesso
  const bot = await BotModel.findById(botId);
  if (!bot) {
    throw new AppError('NOT_FOUND', 'Bot não encontrado', 404);
  }

  if (bot.createdBy !== userId && bot.scope === 'personal') {
    throw new AppError('FORBIDDEN', 'Você não tem permissão para acessar este bot', 403);
  }

  const documents = await Document.find({ botId })
    .sort({ createdAt: -1 })
    .select('-content -embeddings'); // Não retornar conteúdo completo

  res.json({
    success: true,
    data: documents,
  });
}

/**
 * Obter documento específico
 */
export async function getDocumentById(req: Request, res: Response): Promise<void> {
  const { id } = req.params;
  const userId = (req as any).user?.userId;

  const document = await Document.findById(id);
  if (!document) {
    throw new AppError('NOT_FOUND', 'Documento não encontrado', 404);
  }

  // Verificar permissão através do bot
  const bot = await BotModel.findById(document.botId);
  if (!bot || (bot.createdBy !== userId && bot.scope === 'personal')) {
    throw new AppError('FORBIDDEN', 'Você não tem permissão para acessar este documento', 403);
  }

  res.json({
    success: true,
    data: document,
  });
}

/**
 * Deletar documento
 */
export async function deleteDocument(req: Request, res: Response): Promise<void> {
  const { id } = req.params;
  const userId = (req as any).user?.userId;

  const document = await Document.findById(id);
  if (!document) {
    throw new AppError('NOT_FOUND', 'Documento não encontrado', 404);
  }

  // Verificar permissão através do bot
  const bot = await BotModel.findById(document.botId);
  if (!bot || bot.createdBy !== userId) {
    throw new AppError('FORBIDDEN', 'Você não tem permissão para deletar este documento', 403);
  }

  await document.deleteOne();

  logger.info(`Documento ${id} deletado por ${userId}`);

  res.json({
    success: true,
    message: 'Documento deletado com sucesso',
  });
}
