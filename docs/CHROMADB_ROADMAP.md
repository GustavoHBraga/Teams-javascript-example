# 🗺️ Roadmap de Implementação ChromaDB

## Guia passo a passo para implementar Vector Database no seu projeto

---

## 📋 Checklist Completo

### **Fase 1: Setup Inicial** ⏱️ 30 minutos

- [ ] **Passo 1.1:** Iniciar ChromaDB
  ```bash
  docker run -d -p 8000:8000 --name chromadb chromadb/chroma:latest
  ```

- [ ] **Passo 1.2:** Verificar ChromaDB rodando
  ```bash
  curl http://localhost:8000/api/v1/heartbeat
  ```

- [ ] **Passo 1.3:** Instalar dependências
  ```bash
  cd packages/api
  npm install chromadb @langchain/community pdf-parse mammoth
  ```

- [ ] **Passo 1.4:** Adicionar variáveis de ambiente
  ```env
  CHROMADB_URL=http://localhost:8000
  RAG_CHUNK_SIZE=1000
  RAG_CHUNK_OVERLAP=200
  RAG_TOP_K=5
  ```

---

### **Fase 2: Serviços Core** ⏱️ 1 hora

- [ ] **Passo 2.1:** Criar `chromadb.service.ts`
  - Copiar de: [CHROMADB_IMPLEMENTATION.md](./CHROMADB_IMPLEMENTATION.md#4-chromadb-service-completo)
  - Localização: `packages/api/src/services/chromadb.service.ts`
  - Métodos principais:
    - `getOrCreateCollection()`
    - `addDocuments()`
    - `searchSimilar()`
    - `deleteDocuments()`

- [ ] **Passo 2.2:** Atualizar `ai.service.ts`
  - Adicionar método `generateEmbeddings()`
  - Suporte para batch processing
  - Rate limiting para OpenAI

- [ ] **Passo 2.3:** Atualizar `rag.service.ts`
  - Método `processDocument()` completo
  - Extração de texto (PDF, DOCX, TXT)
  - Chunking com LangChain
  - Integração com ChromaDB

---

### **Fase 3: Controllers e Routes** ⏱️ 45 minutos

- [ ] **Passo 3.1:** Atualizar `chat.controller.ts`
  - Buscar contexto com `ragService.searchRelevantDocuments()`
  - Injetar contexto no prompt
  - Retornar info sobre uso do RAG

- [ ] **Passo 3.2:** Atualizar `document.controller.ts`
  - Processamento assíncrono de documentos
  - Feedback de status para frontend

- [ ] **Passo 3.3:** Criar health check routes
  - `/health` - Status geral
  - `/health/chromadb` - ChromaDB específico
  - `/health/rag` - Estatísticas RAG

---

### **Fase 4: Frontend Integration** ⏱️ 30 minutos

- [ ] **Passo 4.1:** Atualizar `BotCreator.tsx`
  - Switch para "Habilitar RAG"
  - Componente DocumentUploader já criado ✅

- [ ] **Passo 4.2:** Atualizar `BotChat.tsx`
  - Mostrar indicador quando RAG é usado
  - Badge "📚 Usando documentos" na resposta

- [ ] **Passo 4.3:** Criar página de gestão de documentos
  - Listar documentos do bot
  - Status de processamento
  - Reprocessar documentos
  - Deletar documentos

---

### **Fase 5: Testing** ⏱️ 1 hora

- [ ] **Passo 5.1:** Teste manual completo
  ```powershell
  .\test-chromadb.ps1
  ```

- [ ] **Passo 5.2:** Testes unitários
  - `chromadb.service.test.ts`
  - `rag.service.test.ts`
  - Mock do ChromaDB client

- [ ] **Passo 5.3:** Testes de integração
  - Upload → Processamento → Busca
  - Múltiplos documentos
  - Diferentes formatos

- [ ] **Passo 5.4:** Testes de performance
  - Tempo de processamento
  - Latência de busca
  - Qualidade dos resultados

---

### **Fase 6: Monitoring e Logs** ⏱️ 30 minutos

- [ ] **Passo 6.1:** Adicionar logs detalhados
  - Início/fim de processamento
  - Tempo de cada etapa
  - Quantidade de chunks/embeddings

- [ ] **Passo 6.2:** Criar dashboard de métricas
  - Documentos processados
  - Taxa de sucesso
  - Tempo médio
  - Queries por minuto

- [ ] **Passo 6.3:** Alertas
  - ChromaDB down
  - Processamento falhando
  - Latência alta

---

### **Fase 7: Otimizações** ⏱️ 2 horas

- [ ] **Passo 7.1:** Cache de embeddings
  - Evitar regerar embeddings iguais
  - Redis ou in-memory cache

- [ ] **Passo 7.2:** Batch processing
  - Processar múltiplos documentos em paralelo
  - Queue com Bull ou BullMQ

- [ ] **Passo 7.3:** Reranking
  - Melhorar ordem dos resultados
  - Considerar data, relevância, etc.

- [ ] **Passo 7.4:** Filtros avançados
  - Por tipo de documento
  - Por data de upload
  - Por tags/categorias

---

### **Fase 8: Documentação** ⏱️ 1 hora

- [ ] **Passo 8.1:** Documentar arquitetura
  - Diagrama de fluxo
  - Decisões técnicas
  - Trade-offs

- [ ] **Passo 8.2:** Guia de troubleshooting
  - Problemas comuns
  - Soluções
  - FAQs

- [ ] **Passo 8.3:** Runbook operacional
  - Como reiniciar ChromaDB
  - Como reprocessar documentos
  - Como fazer backup

---

## 📊 Estimativa de Tempo Total

| Fase | Tempo | Complexidade |
|------|-------|--------------|
| 1. Setup Inicial | 30 min | 🟢 Fácil |
| 2. Serviços Core | 1 hora | 🟡 Média |
| 3. Controllers/Routes | 45 min | 🟡 Média |
| 4. Frontend | 30 min | 🟢 Fácil |
| 5. Testing | 1 hora | 🟡 Média |
| 6. Monitoring | 30 min | 🟢 Fácil |
| 7. Otimizações | 2 horas | 🔴 Difícil |
| 8. Documentação | 1 hora | 🟢 Fácil |
| **TOTAL** | **~7.5 horas** | |

---

## 🎯 Milestones

### **Milestone 1: MVP (3 horas)**
✅ ChromaDB rodando  
✅ Upload e processamento básico  
✅ Busca funcionando  
✅ Chat usando RAG  

### **Milestone 2: Production Ready (6 horas)**
✅ Todos os formatos de arquivo  
✅ Error handling robusto  
✅ Logs e monitoring  
✅ Testes básicos  

### **Milestone 3: Otimizado (8+ horas)**
✅ Performance otimizada  
✅ Cache implementado  
✅ Reranking avançado  
✅ Documentação completa  

---

## 🚀 Quick Start (Mínimo Viável)

Se você quer apenas testar rapidamente (1 hora):

```bash
# 1. ChromaDB
docker run -d -p 8000:8000 chromadb/chroma

# 2. Dependências
npm install chromadb

# 3. Copiar código mínimo
# Ver: QUICK_CHROMADB.md

# 4. Testar
# Upload um .txt via frontend
# Fazer pergunta no chat
# ✅ Funciona!
```

---

## 📝 Notas de Implementação

### **Importante Saber**

1. **Embeddings custam dinheiro**
   - OpenAI: $0.02 / 1M tokens
   - Calcule: ~50k tokens = $0.001
   - 100 documentos ≈ $0.10

2. **Processamento é assíncrono**
   - Upload retorna imediatamente
   - Processamento em background
   - Status: processing → completed

3. **Chunks são importantes**
   - Tamanho ideal: 500-1500 caracteres
   - Overlap: 10-20% do tamanho
   - Mais chunks = mais precisão (e custo)

4. **ChromaDB escala bem até 1M vetores**
   - Após isso, considere Pinecone/Milvus
   - Ou shard collections por bot

### **Decisões Arquiteturais**

| Decisão | Escolha | Motivo |
|---------|---------|--------|
| Vector DB | ChromaDB | Open source, simples |
| Embedding Model | text-embedding-3-small | Custo-benefício |
| Chunk Size | 1000 chars | Balance precisão/custo |
| Overlap | 200 chars | Contexto entre chunks |
| Top K | 5 chunks | Suficiente para contexto |
| Min Score | 0.7 | Filtrar resultados ruins |

---

## 🐛 Troubleshooting Comum

### **ChromaDB não conecta**
```bash
# Verificar se está rodando
docker ps | grep chroma

# Reiniciar
docker restart chromadb

# Logs
docker logs chromadb
```

### **Embeddings falham**
```
Erro: Rate limit exceeded
```
Solução: Adicionar retry com backoff exponencial

### **Busca não retorna resultados**
Possíveis causas:
- Documentos ainda processando
- Min score muito alto
- Embeddings não gerados

### **Performance ruim**
Otimizações:
- Aumentar chunk size
- Reduzir overlap
- Usar cache
- Batch processing

---

## 📚 Recursos Extras

### **Leitura Recomendada**
- [Vector Database Explained](https://www.pinecone.io/learn/vector-database/)
- [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)
- [LangChain RAG Tutorial](https://js.langchain.com/docs/use_cases/question_answering/)

### **Vídeos**
- [What is RAG?](https://www.youtube.com/watch?v=T-D1OfcDW1M)
- [ChromaDB Tutorial](https://www.youtube.com/watch?v=QdDoFfkVkcw)

### **Ferramentas Úteis**
- [Chroma UI](https://github.com/flanker/chroma-ui) - Interface visual
- [Embedding Visualizer](https://projector.tensorflow.org/) - Ver embeddings

---

## ✅ Validação Final

Antes de considerar completo, verifique:

- [ ] ChromaDB está persistindo dados (não perde ao reiniciar)
- [ ] Todos os formatos de arquivo funcionam (PDF, DOCX, TXT)
- [ ] Busca retorna resultados relevantes
- [ ] Chat usa contexto dos documentos
- [ ] Erros são tratados gracefully
- [ ] Logs ajudam no debug
- [ ] Performance é aceitável (< 2s de upload a resposta)
- [ ] Documentação está clara

---

## 🎉 Próximos Passos Após Implementação

1. **Melhorar Qualidade**
   - Fine-tune chunk size para seu caso
   - Experimentar diferentes embedding models
   - Implementar reranking

2. **Escalar**
   - Migrar para Pinecone se necessário
   - Implementar sharding
   - Adicionar caching agressivo

3. **Monitorar**
   - Dashboard de métricas
   - Alertas automáticos
   - Feedback dos usuários

4. **Iterar**
   - A/B testing de parâmetros
   - Coletar feedback
   - Otimizar continuamente

---

**Boa implementação!** 🚀

Dúvidas? Consulte os outros guias:
- [VECTOR_DATABASE_GUIDE.md](./VECTOR_DATABASE_GUIDE.md) - Detalhes técnicos
- [CHROMADB_IMPLEMENTATION.md](./CHROMADB_IMPLEMENTATION.md) - Código completo
- [QUICK_CHROMADB.md](./QUICK_CHROMADB.md) - Setup rápido
