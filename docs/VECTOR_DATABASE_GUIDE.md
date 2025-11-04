# 🧠 Melhorando o RAG com Vector Database (ChromaDB)

## 📋 Visão Geral

Este guia explica como **evoluir o sistema RAG** do básico para um sistema profissional usando **ChromaDB** (Vector Database) para busca semântica avançada.

---

## 🎯 O Que é Vector Database?

### **Conceito**

Um **Vector Database** armazena dados como **vetores** (embeddings) que representam o significado semântico do texto. Isso permite buscar por **similaridade de significado**, não apenas palavras-chave.

### **Diferença: Busca Tradicional vs Busca Vetorial**

```
🔍 BUSCA TRADICIONAL (Keyword):
Usuário: "Como fazer deploy?"
Sistema: Busca por "deploy" no texto
Resultado: Só encontra se a palavra exata existir

🎯 BUSCA VETORIAL (Semântica):
Usuário: "Como fazer deploy?"
Sistema: Entende o significado
Resultado: Encontra também "publicar aplicação", 
          "enviar para produção", "release"
```

### **Por que ChromaDB?**

- ✅ **Open Source** e gratuito
- ✅ **Fácil instalação** (Python ou Docker)
- ✅ **API simples** (REST ou SDK)
- ✅ **Rápido** para datasets médios
- ✅ **Persistência** local ou cloud
- ✅ **Integração** com LangChain
- ✅ **Metadados** ricos para filtragem

---

## 🏗️ Arquitetura Atual vs Melhorada

### **ANTES (Básico)**

```
Documento → MongoDB → Busca por palavras-chave
                   ↓
              Resultados limitados
```

### **DEPOIS (Com ChromaDB)**

```
Documento → Extração de texto → Chunking
                                    ↓
                           OpenAI Embeddings
                                    ↓
                              ChromaDB (vetores)
                                    ↓
Pergunta → Embedding → Busca semântica → Top K resultados
                                              ↓
                                        Contexto para LLM
```

---

## 📦 Instalação e Setup

### **1. Instalar Dependências**

```bash
# Backend (API)
cd packages/api
npm install chromadb @langchain/community pdf-parse mammoth

# Ou com yarn
yarn add chromadb @langchain/community pdf-parse mammoth
```

### **2. Iniciar ChromaDB Server**

#### **Opção A: Docker (Recomendado)**

```bash
# Baixar e rodar ChromaDB
docker run -d -p 8000:8000 chromadb/chroma:latest
```

#### **Opção B: Python Local**

```bash
# Instalar ChromaDB
pip install chromadb

# Rodar servidor
chroma run --host localhost --port 8000
```

#### **Opção C: Cloud (Produção)**

```bash
# Usar ChromaDB Cloud (https://www.trychroma.com)
# Ou hospedar no Railway/Render
```

### **3. Verificar ChromaDB**

```bash
# Testar conexão
curl http://localhost:8000/api/v1/heartbeat

# Resposta esperada:
{"nanosecond heartbeat": 1234567890}
```

---

## 🔧 Configuração

### **1. Variáveis de Ambiente**

```env
# packages/api/.env

# ChromaDB
CHROMADB_URL=http://localhost:8000
CHROMADB_API_KEY=  # Opcional para ChromaDB Cloud

# OpenAI (para embeddings)
OPENAI_API_KEY=sk-...

# Configurações RAG
RAG_CHUNK_SIZE=1000
RAG_CHUNK_OVERLAP=200
RAG_TOP_K=5
```

### **2. Configuração TypeScript**

```typescript
// packages/api/src/config/index.ts

export const config = {
  // ... outras configs
  
  chromadb: {
    url: process.env.CHROMADB_URL || 'http://localhost:8000',
    apiKey: process.env.CHROMADB_API_KEY,
  },
  
  rag: {
    chunkSize: parseInt(process.env.RAG_CHUNK_SIZE || '1000', 10),
    chunkOverlap: parseInt(process.env.RAG_CHUNK_OVERLAP || '200', 10),
    topK: parseInt(process.env.RAG_TOP_K || '5', 10),
  },
};
```

---

## 💻 Implementação

### **1. Criar ChromaDB Service**

```typescript
// packages/api/src/services/chromadb.service.ts

import { ChromaClient } from 'chromadb';
import { config } from '../config';
import { logger } from '../utils/logger';

export class ChromaDBService {
  private client: ChromaClient;
  private collectionName = 'bot-documents';

  constructor() {
    this.client = new ChromaClient({
      path: config.chromadb.url,
    });
  }

  /**
   * Inicializar ou obter collection
   */
  async getOrCreateCollection(botId: string) {
    try {
      const collectionName = `bot_${botId}`;
      
      const collection = await this.client.getOrCreateCollection({
        name: collectionName,
        metadata: { botId },
      });

      logger.info(`Collection ${collectionName} ready`);
      return collection;
    } catch (error) {
      logger.error('Error getting collection:', error);
      throw error;
    }
  }

  /**
   * Adicionar documentos com embeddings
   */
  async addDocuments(
    botId: string,
    documents: {
      id: string;
      text: string;
      embedding: number[];
      metadata: Record<string, any>;
    }[]
  ) {
    try {
      const collection = await this.getOrCreateCollection(botId);

      await collection.add({
        ids: documents.map(d => d.id),
        embeddings: documents.map(d => d.embedding),
        documents: documents.map(d => d.text),
        metadatas: documents.map(d => d.metadata),
      });

      logger.info(`Added ${documents.length} documents to ChromaDB`);
    } catch (error) {
      logger.error('Error adding documents:', error);
      throw error;
    }
  }

  /**
   * Buscar documentos similares
   */
  async searchSimilar(
    botId: string,
    queryEmbedding: number[],
    topK: number = 5
  ) {
    try {
      const collection = await this.getOrCreateCollection(botId);

      const results = await collection.query({
        queryEmbeddings: [queryEmbedding],
        nResults: topK,
      });

      return results;
    } catch (error) {
      logger.error('Error searching documents:', error);
      throw error;
    }
  }

  /**
   * Deletar documentos
   */
  async deleteDocuments(botId: string, documentIds: string[]) {
    try {
      const collection = await this.getOrCreateCollection(botId);

      await collection.delete({
        ids: documentIds,
      });

      logger.info(`Deleted ${documentIds.length} documents from ChromaDB`);
    } catch (error) {
      logger.error('Error deleting documents:', error);
      throw error;
    }
  }

  /**
   * Deletar collection inteira (quando bot é deletado)
   */
  async deleteCollection(botId: string) {
    try {
      const collectionName = `bot_${botId}`;
      await this.client.deleteCollection({ name: collectionName });
      logger.info(`Collection ${collectionName} deleted`);
    } catch (error) {
      logger.error('Error deleting collection:', error);
      throw error;
    }
  }
}

export const chromaDBService = new ChromaDBService();
```

### **2. Melhorar RAG Service**

```typescript
// packages/api/src/services/rag.service.ts

import { chromaDBService } from './chromadb.service';
import { aiService } from './ai.service';
import { DocumentModel } from '../database/models';
import { logger } from '../utils/logger';
import { config } from '../config';
import { RecursiveCharacterTextSplitter } from 'langchain/text_splitter';
import pdfParse from 'pdf-parse';
import mammoth from 'mammoth';

export class RAGService {
  /**
   * Processar documento completo
   */
  async processDocument(
    botId: string,
    document: {
      id: string;
      file: Buffer;
      filename: string;
      mimeType: string;
      metadata?: any;
    }
  ): Promise<void> {
    try {
      logger.info(`Processing document ${document.id} for bot ${botId}`);

      // 1. Extrair texto do arquivo
      const text = await this.extractText(document.file, document.mimeType);

      // 2. Dividir em chunks
      const chunks = await this.splitIntoChunks(text);

      // 3. Gerar embeddings para cada chunk
      const embeddings = await aiService.generateEmbeddings(
        chunks.map(c => c.pageContent)
      );

      // 4. Preparar documentos para ChromaDB
      const chromaDocuments = chunks.map((chunk, index) => ({
        id: `${document.id}_chunk_${index}`,
        text: chunk.pageContent,
        embedding: embeddings[index],
        metadata: {
          documentId: document.id,
          filename: document.filename,
          chunkIndex: index,
          totalChunks: chunks.length,
          ...document.metadata,
        },
      }));

      // 5. Adicionar ao ChromaDB
      await chromaDBService.addDocuments(botId, chromaDocuments);

      // 6. Atualizar documento no MongoDB
      await DocumentModel.findByIdAndUpdate(document.id, {
        status: 'completed',
        processedAt: new Date(),
        chunks: chunks.map(c => c.pageContent),
        metadata: {
          totalChunks: chunks.length,
          vectorized: true,
          ...document.metadata,
        },
      });

      logger.info(`Document ${document.id} processed successfully`);
    } catch (error) {
      logger.error('Error processing document:', error);
      
      // Atualizar status para failed
      await DocumentModel.findByIdAndUpdate(document.id, {
        status: 'failed',
        metadata: {
          error: error instanceof Error ? error.message : 'Unknown error',
        },
      });

      throw error;
    }
  }

  /**
   * Extrair texto de diferentes formatos
   */
  private async extractText(buffer: Buffer, mimeType: string): Promise<string> {
    try {
      switch (mimeType) {
        case 'application/pdf':
          const pdfData = await pdfParse(buffer);
          return pdfData.text;

        case 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
          const docxData = await mammoth.extractRawText({ buffer });
          return docxData.value;

        case 'text/plain':
        case 'text/markdown':
          return buffer.toString('utf-8');

        default:
          throw new Error(`Unsupported file type: ${mimeType}`);
      }
    } catch (error) {
      logger.error('Error extracting text:', error);
      throw error;
    }
  }

  /**
   * Dividir texto em chunks usando LangChain
   */
  private async splitIntoChunks(text: string) {
    const splitter = new RecursiveCharacterTextSplitter({
      chunkSize: config.rag.chunkSize,
      chunkOverlap: config.rag.chunkOverlap,
      separators: ['\n\n', '\n', '. ', '! ', '? ', ', ', ' ', ''],
    });

    return await splitter.createDocuments([text]);
  }

  /**
   * Buscar documentos relevantes usando busca semântica
   */
  async searchRelevantDocuments(
    botId: string,
    query: string,
    topK: number = 5
  ) {
    try {
      // 1. Gerar embedding da pergunta
      const [queryEmbedding] = await aiService.generateEmbeddings([query]);

      // 2. Buscar no ChromaDB
      const results = await chromaDBService.searchSimilar(
        botId,
        queryEmbedding,
        topK
      );

      // 3. Formatar resultados
      if (!results.documents || !results.documents[0]) {
        return [];
      }

      return results.documents[0].map((doc, index) => ({
        content: doc,
        metadata: results.metadatas?.[0]?.[index] || {},
        distance: results.distances?.[0]?.[index] || 0,
      }));
    } catch (error) {
      logger.error('Error searching documents:', error);
      return [];
    }
  }

  /**
   * Deletar documentos do bot
   */
  async deleteDocuments(botId: string, documentIds: string[]) {
    try {
      // Buscar chunks relacionados no MongoDB
      const documents = await DocumentModel.find({
        _id: { $in: documentIds },
        botId,
      });

      // Gerar IDs de todos os chunks
      const chunkIds: string[] = [];
      documents.forEach(doc => {
        const totalChunks = doc.metadata?.totalChunks || 0;
        for (let i = 0; i < totalChunks; i++) {
          chunkIds.push(`${doc._id}_chunk_${i}`);
        }
      });

      // Deletar do ChromaDB
      if (chunkIds.length > 0) {
        await chromaDBService.deleteDocuments(botId, chunkIds);
      }

      // Deletar do MongoDB
      await DocumentModel.deleteMany({
        _id: { $in: documentIds },
      });

      logger.info(`Deleted ${documentIds.length} documents`);
    } catch (error) {
      logger.error('Error deleting documents:', error);
      throw error;
    }
  }
}

export const ragService = new RAGService();
```

### **3. Atualizar AI Service (Embeddings)**

```typescript
// packages/api/src/services/ai.service.ts

export class AIService {
  // ... código existente

  /**
   * Gerar embeddings para textos
   */
  async generateEmbeddings(texts: string[]): Promise<number[][]> {
    try {
      const response = await this.client.embeddings.create({
        model: 'text-embedding-3-small', // Ou text-embedding-ada-002
        input: texts,
      });

      return response.data.map(item => item.embedding);
    } catch (error) {
      logger.error('Error generating embeddings:', error);
      throw error;
    }
  }
}
```

### **4. Atualizar Chat Service**

```typescript
// packages/api/src/services/chat.service.ts (se existir)
// ou packages/api/src/controllers/chat.controller.ts

async function generateResponse(botId: string, message: string) {
  // 1. Buscar contexto relevante com RAG
  const relevantDocs = await ragService.searchRelevantDocuments(
    botId,
    message,
    config.rag.topK
  );

  // 2. Construir contexto
  const context = relevantDocs
    .map((doc, i) => `[Documento ${i + 1}]\n${doc.content}`)
    .join('\n\n');

  // 3. Gerar resposta com contexto
  const prompt = `
Contexto dos documentos anexados:
${context}

Pergunta do usuário: ${message}

Responda baseando-se PRINCIPALMENTE nas informações do contexto acima.
Se a informação não estiver no contexto, mencione isso.
  `.trim();

  const response = await aiService.generateResponse(botId, prompt);
  
  return response;
}
```

---

## 📊 Fluxo Completo

### **Upload e Processamento**

```
1. Usuário faz upload do arquivo
         ↓
2. API salva no MongoDB (status: processing)
         ↓
3. Extrai texto do PDF/DOCX/TXT
         ↓
4. Divide em chunks (1000 caracteres, overlap 200)
         ↓
5. Gera embeddings com OpenAI (cada chunk → vetor)
         ↓
6. Salva vetores no ChromaDB
         ↓
7. Atualiza MongoDB (status: completed)
```

### **Busca e Resposta**

```
1. Usuário faz pergunta: "Como fazer deploy?"
         ↓
2. Gera embedding da pergunta
         ↓
3. Busca no ChromaDB (similaridade de vetores)
         ↓
4. Retorna Top 5 chunks mais relevantes
         ↓
5. Injeta chunks como contexto no prompt
         ↓
6. LLM gera resposta usando contexto
         ↓
7. Retorna resposta ao usuário
```

---

## 🎯 Exemplo Prático

### **Documento Original**

```markdown
# Runbook - Deploy em Produção

## Pré-requisitos
- Acesso ao Jenkins
- Aprovação do tech lead

## Passo a Passo
1. Acesse https://jenkins.empresa.com
2. Selecione o job "prod-deploy"
3. Clique em "Build with Parameters"
4. Escolha a versão (git tag)
5. Confirme e aguarde

## Rollback
Em caso de problemas:
1. Acesse job "prod-rollback"
2. Selecione versão anterior
3. Execute imediatamente
```

### **Processamento**

```
Chunk 1 (ID: doc123_chunk_0):
"Runbook - Deploy em Produção. Pré-requisitos: 
Acesso ao Jenkins, Aprovação do tech lead."
Embedding: [0.23, -0.15, 0.89, ... 1536 dimensões]

Chunk 2 (ID: doc123_chunk_1):
"Passo a Passo: 1. Acesse https://jenkins.empresa.com
2. Selecione o job prod-deploy..."
Embedding: [0.45, 0.12, -0.34, ... 1536 dimensões]

Chunk 3 (ID: doc123_chunk_2):
"Rollback: Em caso de problemas, acesse job 
prod-rollback, selecione versão anterior..."
Embedding: [-0.11, 0.67, 0.23, ... 1536 dimensões]
```

### **Busca**

```typescript
// Usuário pergunta
const query = "Como fazer rollback da aplicação?";

// Sistema gera embedding da pergunta
const queryEmbedding = await aiService.generateEmbeddings([query]);
// [−0.08, 0.71, 0.19, ... 1536 dimensões]

// Busca no ChromaDB (similaridade de cosseno)
const results = await chromaDBService.searchSimilar('bot123', queryEmbedding, 3);

// Resultado ordenado por similaridade:
// 1. Chunk 3 (distance: 0.92) ← Mais similar!
// 2. Chunk 2 (distance: 0.67)
// 3. Chunk 1 (distance: 0.34)
```

### **Resposta**

```
[Sistema injeta Chunk 3 como contexto]

Contexto: "Rollback: Em caso de problemas, acesse job 
prod-rollback, selecione versão anterior..."

Pergunta: "Como fazer rollback da aplicação?"

GPT-4 responde:
"Com base no runbook do seu squad, para fazer rollback 
da aplicação você deve:

1. Acessar o Jenkins
2. Buscar pelo job 'prod-rollback'
3. Selecionar a versão anterior estável
4. Executar o job imediatamente

Este processo é recomendado quando houver problemas 
após um deploy em produção."
```

---

## 📈 Comparação de Performance

### **Antes (Busca por Palavras-chave)**

```
Pergunta: "Como reverter uma publicação?"

MongoDB busca: "reverter" OR "publicação"
Resultado: ❌ Nada encontrado (palavras exatas não existem)
```

### **Depois (Busca Semântica)**

```
Pergunta: "Como reverter uma publicação?"

ChromaDB busca: Similaridade vetorial
Entende que:
- "reverter" ≈ "rollback"
- "publicação" ≈ "deploy"

Resultado: ✅ Encontra seção de rollback!
```

---

## 🔍 Monitoramento e Debug

### **1. Verificar ChromaDB**

```typescript
// Listar collections
const collections = await chromaDBService.client.listCollections();
console.log('Collections:', collections);

// Ver quantidade de documentos
const collection = await chromaDBService.getOrCreateCollection('bot123');
const count = await collection.count();
console.log(`Bot123 has ${count} chunks`);
```

### **2. Testar Busca**

```typescript
// Teste direto
const results = await ragService.searchRelevantDocuments(
  'bot123',
  'teste de pergunta',
  3
);

console.log('Resultados:', results);
// [
//   { content: '...', metadata: {...}, distance: 0.89 },
//   { content: '...', metadata: {...}, distance: 0.67 },
// ]
```

### **3. Logs Detalhados**

```typescript
// Adicionar logs no RAG Service
logger.debug('Chunks gerados:', { count: chunks.length });
logger.debug('Embeddings gerados:', { count: embeddings.length });
logger.debug('Busca retornou:', { results: results.length });
```

---

## 💰 Custos e Limites

### **OpenAI Embeddings**

| Modelo | Custo | Dimensões | Uso |
|--------|-------|-----------|-----|
| text-embedding-3-small | $0.02 / 1M tokens | 1536 | Recomendado |
| text-embedding-3-large | $0.13 / 1M tokens | 3072 | Maior precisão |
| text-embedding-ada-002 | $0.10 / 1M tokens | 1536 | Legado |

**Exemplo de custo:**
- 10 documentos = ~50k tokens
- Custo: $0.001 (menos de 1 centavo!)

### **ChromaDB**

- ✅ **Open source**: Grátis
- ✅ **Self-hosted**: Apenas custo de servidor
- ✅ **Cloud (opcional)**: A partir de $29/mês

---

## 🚀 Otimizações Avançadas

### **1. Cache de Embeddings**

```typescript
// Evitar regerar embeddings para mesmos textos
const cache = new Map<string, number[]>();

async function getCachedEmbedding(text: string) {
  const hash = crypto.createHash('sha256').update(text).digest('hex');
  
  if (cache.has(hash)) {
    return cache.get(hash)!;
  }
  
  const [embedding] = await aiService.generateEmbeddings([text]);
  cache.set(hash, embedding);
  
  return embedding;
}
```

### **2. Batch Processing**

```typescript
// Processar múltiplos documentos em paralelo
async function processMultipleDocuments(botId: string, documents: any[]) {
  const batchSize = 5;
  
  for (let i = 0; i < documents.length; i += batchSize) {
    const batch = documents.slice(i, i + batchSize);
    
    await Promise.all(
      batch.map(doc => ragService.processDocument(botId, doc))
    );
  }
}
```

### **3. Reranking**

```typescript
// Melhorar qualidade dos resultados com reranking
async function rerankResults(query: string, results: any[]) {
  // Usar modelo de reranking (Cohere, etc)
  // Ou scoring customizado
  
  return results.sort((a, b) => {
    // Priorizar resultados recentes
    const dateScore = (b.metadata.uploadedAt - a.metadata.uploadedAt) * 0.1;
    
    // Combinar com similaridade
    return (b.distance + dateScore) - (a.distance + dateScore);
  });
}
```

### **4. Filtros de Metadata**

```typescript
// Buscar apenas em documentos específicos
async searchSimilar(
  botId: string,
  queryEmbedding: number[],
  filters?: {
    documentType?: string;
    uploadedAfter?: Date;
    tags?: string[];
  }
) {
  const collection = await this.getOrCreateCollection(botId);
  
  const results = await collection.query({
    queryEmbeddings: [queryEmbedding],
    nResults: 5,
    where: {
      // Filtros opcionais
      ...(filters?.documentType && { 
        documentType: filters.documentType 
      }),
      ...(filters?.tags && { 
        tags: { $in: filters.tags } 
      }),
    },
  });
  
  return results;
}
```

---

## 🧪 Testes

### **1. Teste de Processamento**

```typescript
// packages/api/src/__tests__/rag.service.test.ts

describe('RAG Service', () => {
  it('should process PDF document', async () => {
    const buffer = fs.readFileSync('test-docs/sample.pdf');
    
    await ragService.processDocument('test-bot', {
      id: 'test-doc-1',
      file: buffer,
      filename: 'sample.pdf',
      mimeType: 'application/pdf',
    });
    
    // Verificar no MongoDB
    const doc = await DocumentModel.findById('test-doc-1');
    expect(doc.status).toBe('completed');
    expect(doc.chunks).toHaveLength(greaterThan(0));
  });

  it('should find relevant documents', async () => {
    const results = await ragService.searchRelevantDocuments(
      'test-bot',
      'How to deploy?',
      3
    );
    
    expect(results).toHaveLength(3);
    expect(results[0].distance).toBeGreaterThan(0.7);
  });
});
```

### **2. Teste End-to-End**

```bash
# test-rag.ps1

# 1. Upload documento
$response = Invoke-RestMethod -Uri "http://localhost:3001/api/v1/bots/bot123/documents" `
  -Method POST `
  -InFile "runbook.pdf"

# 2. Aguardar processamento
Start-Sleep -Seconds 5

# 3. Fazer pergunta
$chat = Invoke-RestMethod -Uri "http://localhost:3001/api/v1/chat/messages" `
  -Method POST `
  -Body (@{
    botId = "bot123"
    content = "Como fazer deploy?"
  } | ConvertTo-Json)

Write-Host "Resposta: $($chat.data.content)"
```

---

## 📚 Recursos e Referências

### **Documentação Oficial**

- [ChromaDB Docs](https://docs.trychroma.com/)
- [LangChain Text Splitters](https://js.langchain.com/docs/modules/data_connection/document_transformers/)
- [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings)

### **Tutoriais**

- [Building RAG with ChromaDB](https://docs.trychroma.com/guides)
- [Vector Database Best Practices](https://www.pinecone.io/learn/vector-database/)

### **Alternativas ao ChromaDB**

| Banco | Prós | Contras |
|-------|------|---------|
| **Pinecone** | Managed, escalável | Pago ($70+/mês) |
| **Weaviate** | Open source, GraphQL | Complexo |
| **Milvus** | Alta performance | Requer Kubernetes |
| **Qdrant** | Rust, rápido | Menos maduro |
| **Azure AI Search** | Integrado Azure | Vendor lock-in |

---

## ✅ Checklist de Implementação

- [ ] Instalar ChromaDB (Docker ou Python)
- [ ] Adicionar dependências npm
- [ ] Criar ChromaDBService
- [ ] Atualizar RAGService com processamento
- [ ] Implementar extração de texto (PDF/DOCX)
- [ ] Adicionar geração de embeddings
- [ ] Integrar busca semântica no chat
- [ ] Testar com documentos reais
- [ ] Adicionar logs e monitoramento
- [ ] Documentar para equipe

---

## 🎯 Resultado Final

Com essa implementação, você terá:

✅ **Busca Semântica Avançada** - Entende sinônimos e contexto  
✅ **RAG Profissional** - Igual a ChatGPT com seus dados  
✅ **Performance** - Resultados em milissegundos  
✅ **Escalabilidade** - Suporta milhares de documentos  
✅ **Precisão** - Respostas baseadas em fontes reais  

**Seu bot estará pronto para produção!** 🚀
