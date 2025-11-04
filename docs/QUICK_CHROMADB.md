# 🎯 Guia Rápido: ChromaDB Setup em 5 Minutos

## 🚀 Início Rápido

### **1. Instalar Dependências (2 min)**

```bash
cd packages/api
npm install chromadb @langchain/community pdf-parse mammoth
```

### **2. Iniciar ChromaDB (1 min)**

```bash
# Docker (Recomendado)
docker run -d -p 8000:8000 --name chromadb chromadb/chroma:latest

# OU Python
pip install chromadb && chroma run --port 8000
```

### **3. Configurar .env (30 seg)**

```env
# packages/api/.env
CHROMADB_URL=http://localhost:8000
RAG_CHUNK_SIZE=1000
RAG_CHUNK_OVERLAP=200
RAG_TOP_K=5
```

### **4. Criar Arquivos (1 min)**

#### **chromadb.service.ts**

```typescript
import { ChromaClient } from 'chromadb';

export class ChromaDBService {
  private client = new ChromaClient({ path: process.env.CHROMADB_URL });

  async addDocuments(botId: string, docs: any[]) {
    const collection = await this.client.getOrCreateCollection({ 
      name: `bot_${botId}` 
    });
    
    await collection.add({
      ids: docs.map(d => d.id),
      embeddings: docs.map(d => d.embedding),
      documents: docs.map(d => d.text),
      metadatas: docs.map(d => d.metadata),
    });
  }

  async search(botId: string, queryEmbedding: number[], topK = 5) {
    const collection = await this.client.getOrCreateCollection({ 
      name: `bot_${botId}` 
    });
    
    return await collection.query({
      queryEmbeddings: [queryEmbedding],
      nResults: topK,
    });
  }
}

export const chromaDBService = new ChromaDBService();
```

### **5. Usar no RAG Service (30 seg)**

```typescript
// Atualizar rag.service.ts

async processDocument(botId: string, document: any) {
  // 1. Extrair texto
  const text = document.file.toString('utf-8');
  
  // 2. Dividir em chunks
  const chunks = this.chunkText(text, 1000);
  
  // 3. Gerar embeddings
  const embeddings = await aiService.generateEmbeddings(chunks);
  
  // 4. Salvar no ChromaDB
  await chromaDBService.addDocuments(botId, 
    chunks.map((chunk, i) => ({
      id: `${document.id}_chunk_${i}`,
      text: chunk,
      embedding: embeddings[i],
      metadata: { documentId: document.id, chunkIndex: i }
    }))
  );
}

async searchRelevantDocuments(botId: string, query: string) {
  // 1. Gerar embedding da pergunta
  const [queryEmbedding] = await aiService.generateEmbeddings([query]);
  
  // 2. Buscar no ChromaDB
  const results = await chromaDBService.search(botId, queryEmbedding, 5);
  
  return results.documents[0];
}
```

### **6. Testar (30 seg)**

```bash
# Verificar ChromaDB
curl http://localhost:8000/api/v1/heartbeat

# Fazer upload de documento via frontend
# Fazer pergunta no chat
# Bot responde usando RAG com ChromaDB! ✅
```

---

## 🎯 Pronto!

Agora seu sistema tem:
- ✅ Busca semântica profissional
- ✅ RAG com Vector Database
- ✅ Performance otimizada
- ✅ Escalabilidade garantida

**Tempo total: ~5 minutos** ⚡

Para detalhes completos, veja [VECTOR_DATABASE_GUIDE.md](./VECTOR_DATABASE_GUIDE.md)
