import { DocumentSource, DocumentStatus } from '@teams-bot/shared';

import { logger } from '../utils/logger';
import { DocumentModel } from '../database/models';

/**
 * RAG Service - Retrieval Augmented Generation
 * Handles document indexing and retrieval for context-aware responses
 */
export class RAGService {
  /**
   * Process document and generate embeddings
   */
  async processDocument(
    botId: string,
    document: { id: string; content: string; metadata?: any }
  ): Promise<void> {
    try {
      logger.info(`Processing document ${document.id} for bot ${botId}`);

      // Dividir documento em chunks (pedaços menores para melhor busca)
      const chunks = this.chunkText(document.content, 1000); // 1000 caracteres por chunk

      // TODO: Gerar embeddings para cada chunk
      // const embeddings = await this.aiService.generateEmbeddings(chunks);

      // Atualizar documento com chunks e embeddings
      await DocumentModel.findByIdAndUpdate(document.id, {
        chunks,
        // embeddings, // Será adicionado quando implementar geração de embeddings
        status: DocumentStatus.COMPLETED,
        processedAt: new Date(),
      });

      logger.info(`Document ${document.id} processed successfully`);
    } catch (error) {
      logger.error('Error processing document:', error);
      throw error;
    }
  }

  /**
   * Divide texto em chunks menores
   */
  private chunkText(text: string, chunkSize: number): string[] {
    const chunks: string[] = [];
    const sentences = text.split(/[.!?]+\s+/); // Dividir por sentenças
    
    let currentChunk = '';
    
    for (const sentence of sentences) {
      if ((currentChunk + sentence).length <= chunkSize) {
        currentChunk += sentence + '. ';
      } else {
        if (currentChunk) {
          chunks.push(currentChunk.trim());
        }
        currentChunk = sentence + '. ';
      }
    }
    
    if (currentChunk) {
      chunks.push(currentChunk.trim());
    }
    
    return chunks;
  }

  /**
   * Search for relevant documents based on a query
   */
  async searchDocuments(botId: string, query: string, topK: number = 5): Promise<DocumentSource[]> {
    try {
      logger.info('Searching documents for RAG', { botId, query, topK });

      // Generate embeddings for the query (for future vector search)
      // const queryEmbedding = await aiService.generateEmbeddings(query);

      // Find documents for this bot
      const documents = await DocumentModel.find({
        botId,
        status: 'completed',
      }).limit(50); // Limit to avoid processing too many docs

      if (documents.length === 0) {
        logger.info('No documents found for bot', { botId });
        return [];
      }

      // For now, we'll do a simple keyword-based search
      // In production, you would use Azure AI Search or a vector database
      const results: DocumentSource[] = [];

      for (const doc of documents) {
        // Simple keyword matching (replace with vector similarity in production)
        const keywords = query.toLowerCase().split(' ');
        const nameMatch = keywords.some((keyword) =>
          doc.name.toLowerCase().includes(keyword)
        );

        if (nameMatch || results.length < topK) {
          results.push({
            documentId: doc._id.toString(),
            documentName: doc.name,
            snippet: `Content from ${doc.name}`, // In production, extract actual content
            score: nameMatch ? 0.8 : 0.5,
          });
        }
      }

      // Sort by score and limit to topK
      const sorted = results.sort((a, b) => b.score - a.score);
      return sorted.slice(0, topK);
    } catch (error) {
      logger.error('Error searching documents:', error);
      // Return empty array rather than failing - bot can still respond without context
      return [];
    }
  }

  /**
   * Index a document for RAG
   * In production, this would:
   * 1. Extract text from the document
   * 2. Split into chunks
   * 3. Generate embeddings for each chunk
   * 4. Store in Azure AI Search or vector database
   */
  async indexDocument(documentId: string): Promise<void> {
    try {
      logger.info('Indexing document', { documentId });

      const document = await DocumentModel.findById(documentId);
      if (!document) {
        throw new Error('Document not found');
      }

      // TODO: Implement actual document processing
      // 1. Download document from storage
      // 2. Extract text (using pdf-parse, mammoth, etc.)
      // 3. Split into chunks
      // 4. Generate embeddings
      // 5. Store in vector database

      // For now, just mark as completed
      document.status = DocumentStatus.COMPLETED;
      document.vectorIndexId = `index-${documentId}`;
      await document.save();

      logger.info('Document indexed successfully', { documentId });
    } catch (error) {
      logger.error('Error indexing document:', error);
      
      // Update document status to failed
      await DocumentModel.findByIdAndUpdate(documentId, {
        status: DocumentStatus.FAILED,
      });

      throw error;
    }
  }

  /**
   * Delete document from index
   */
  async deleteDocumentIndex(documentId: string): Promise<void> {
    try {
      logger.info('Deleting document index', { documentId });

      const document = await DocumentModel.findById(documentId);
      if (!document?.vectorIndexId) {
        return;
      }

      // TODO: Delete from vector database
      // For now, just remove the vectorIndexId
      document.vectorIndexId = undefined;
      await document.save();

      logger.info('Document index deleted', { documentId });
    } catch (error) {
      logger.error('Error deleting document index:', error);
      throw error;
    }
  }
}

export const ragService = new RAGService();
