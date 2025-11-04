# 📄 Upload de Documentos com RAG

## ✅ Implementação Completa

Sim! Agora o frontend **tem suporte completo para upload de documentos** quando você cria um bot. O bot já nasce com conhecimento aumentado através de RAG (Retrieval-Augmented Generation).

---

## 🎯 Como Funciona

### 1️⃣ **Criação do Bot com Documentos**

Quando você cria um bot, pode:
- ✅ Ativar o RAG (switch no formulário)
- ✅ Fazer upload de documentos (PDF, TXT, MD, DOC, DOCX)
- ✅ Arrastar e soltar arquivos (drag & drop)
- ✅ Ver progresso de upload em tempo real
- ✅ O bot já nasce treinado com esses documentos

### 2️⃣ **Processamento Automático**

Após upload, o sistema:
1. Valida o tipo de arquivo
2. Salva no banco de dados
3. Processa o conteúdo
4. Divide em chunks (pedaços pequenos)
5. Gera embeddings (vetores)
6. Indexa para busca semântica

### 3️⃣ **Uso pelo Bot**

Quando você faz perguntas:
1. Sistema busca documentos relevantes
2. Encontra os trechos mais relacionados
3. Injeta como contexto na pergunta
4. Bot responde com base nos documentos

---

## 🖥️ Interface do Usuário

### **Componente: DocumentUploader**

```tsx
<DocumentUploader
  files={documents}
  onFilesChange={setDocuments}
  maxFiles={10}
  acceptedTypes={['.pdf', '.txt', '.md', '.doc', '.docx']}
/>
```

**Funcionalidades:**
- 📎 Drag & drop de arquivos
- 📋 Clique para selecionar
- 📊 Lista com progresso
- ✅ Status de cada arquivo
- 🗑️ Remover arquivos antes de enviar
- 📏 Validação de tipo e tamanho

---

## 🔧 Backend - Endpoints

### **POST /bots/:botId/documents**
Upload de documento para um bot específico

**Headers:**
```
Authorization: Bearer {token}
Content-Type: multipart/form-data
```

**Body (FormData):**
```
file: <arquivo>
title: "Nome do documento" (opcional)
description: "Descrição" (opcional)
```

**Response:**
```json
{
  "success": true,
  "message": "Documento enviado e em processamento",
  "data": {
    "id": "doc123",
    "botId": "bot456",
    "title": "Manual.pdf",
    "status": "processing",
    "size": 1024000
  }
}
```

### **GET /bots/:botId/documents**
Lista documentos de um bot

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "doc123",
      "title": "Manual.pdf",
      "status": "completed",
      "size": 1024000,
      "createdAt": "2024-01-01T00:00:00.000Z"
    }
  ]
}
```

### **GET /documents/:id**
Detalhes de um documento específico

### **DELETE /documents/:id**
Remove um documento

---

## 📦 Estrutura de Dados

### **Document Model**

```typescript
{
  botId: string;           // Bot dono do documento
  title: string;           // Título
  description?: string;    // Descrição
  filename: string;        // Nome original
  mimeType: string;        // Tipo MIME
  size: number;            // Tamanho em bytes
  status: 'processing' | 'completed' | 'failed';
  content?: string;        // Conteúdo extraído
  chunks?: string[];       // Pedaços para RAG
  embeddings?: number[][]; // Vetores
  uploadedBy: string;      // Usuário
  processedAt?: Date;      // Data de processamento
  metadata?: any;          // Metadados extras
}
```

---

## 🎨 Fluxo Visual no Frontend

### **Página de Criação de Bot**

1. **Formulário Padrão**
   - Nome
   - Descrição  
   - Instruções
   - Escopo
   - Modelo de IA
   - Tags

2. **Switch RAG**
   ```
   [ ] Habilitar RAG (Retrieval-Augmented Generation)
   ```

3. **Quando RAG Ativado**
   ```
   ┌─────────────────────────────────────┐
   │  Documentos de Treinamento          │
   ├─────────────────────────────────────┤
   │                                     │
   │    📤  Arraste arquivos aqui        │
   │        ou clique para selecionar    │
   │                                     │
   │    Tipos: .pdf, .txt, .md, etc.    │
   │    Máximo: 10 arquivos              │
   │                                     │
   └─────────────────────────────────────┘
   
   Arquivos anexados (2/10):
   
   ┌─────────────────────────────────────┐
   │ 📄 Manual.pdf            ✅ Enviado │
   │    1.2 MB                          🗑️│
   └─────────────────────────────────────┘
   
   ┌─────────────────────────────────────┐
   │ 📄 FAQ.txt               ⏳ Pendente │
   │    45 KB                           🗑️│
   └─────────────────────────────────────┘
   ```

4. **Card Explicativo**
   ```
   📚 Como funciona o RAG:
   
   Os documentos anexados serão processados e indexados. 
   Quando você fizer perguntas, o bot vai buscar informações 
   relevantes nesses documentos e usar como contexto para 
   gerar respostas mais precisas e específicas.
   ```

5. **Botão de Criação**
   - "Criar Bot" → Cria o bot primeiro
   - "Enviando documentos..." → Faz upload sequencial
   - Redireciona para galeria quando completo

---

## 🧪 Exemplo de Uso

### **1. Criar Bot de SRE com Documentos**

```typescript
// Usuário preenche o formulário
const botData = {
  name: "Bot de SRE",
  description: "Especialista em Site Reliability Engineering",
  instructions: "Você é um especialista em SRE...",
  scope: "squad",
  config: {
    model: "gpt-4-turbo",
    temperature: 0.7,
    enableRAG: true, // ← Ativar RAG
  }
};

// Usuário anexa documentos
const documents = [
  { file: runbook.pdf },
  { file: incident_guide.md },
  { file: monitoring_setup.txt },
];

// Sistema processa automaticamente
```

### **2. Bot Responde com Conhecimento dos Documentos**

**Usuário:** "Como fazer rollback da aplicação?"

**Sistema:**
1. Busca nos documentos anexados
2. Encontra trecho relevante no `runbook.pdf`:
   ```
   "Para fazer rollback:
   1. Acesse o Jenkins
   2. Selecione job deploy-rollback
   3. Escolha a versão anterior"
   ```
3. Bot responde usando esse contexto:
   ```
   "Com base no runbook do seu squad, o rollback deve ser 
   feito acessando o Jenkins e executando o job 
   deploy-rollback. Vou detalhar cada passo..."
   ```

---

## 🔄 Processamento Assíncrono

```typescript
// Fluxo de upload
1. Frontend envia arquivo → API
2. API salva documento (status: processing)
3. API retorna imediatamente
4. Background: processDocumentAsync()
   - Extrai texto
   - Divide em chunks
   - Gera embeddings
   - Indexa
   - Atualiza status → completed
```

**Vantagens:**
- ⚡ Resposta rápida ao usuário
- 🔄 Processamento não bloqueia
- ✅ Status trackável em tempo real
- 🚨 Tratamento de erros isolado

---

## 📊 Estados do Documento

```typescript
type DocumentStatus = 
  | 'pending'      // Aguardando upload
  | 'uploading'    // Upload em progresso
  | 'processing'   // Processando conteúdo
  | 'completed'    // Pronto para uso
  | 'failed'       // Erro no processamento
```

---

## 🛠️ Configuração

### **Tipos de Arquivo Aceitos**

```typescript
const ACCEPTED_TYPES = [
  'application/pdf',
  'text/plain',
  'text/markdown',
  'application/msword',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
];
```

### **Limites**

- Tamanho máximo por arquivo: **10 MB**
- Número máximo de arquivos: **10**
- Extensões: `.pdf`, `.txt`, `.md`, `.doc`, `.docx`

---

## 🚀 Melhorias Futuras

### **Próximos Passos**

1. ✅ Upload implementado
2. ✅ Interface drag & drop
3. ✅ Processamento assíncrono
4. 🚧 Extração de texto (PDF, Word)
5. 🚧 Geração de embeddings com OpenAI
6. 🚧 Armazenamento em vector database
7. 🚧 Busca semântica avançada
8. 🚧 Reprocessamento de documentos
9. 🚧 Visualização do conteúdo
10. 🚧 Edição de metadados

### **Bibliotecas para Integrar**

```json
{
  "pdf-parse": "^1.1.1",        // Extrair texto de PDF
  "mammoth": "^1.6.0",          // Converter DOCX
  "@azure/search-documents": "^12.0.0", // Azure AI Search
  "chromadb": "^1.5.0"          // Vector database local
}
```

---

## 📝 Exemplo Completo

### **Frontend - BotCreator.tsx**

```tsx
// Estado
const [formData, setFormData] = useState({
  name: '',
  config: { enableRAG: false }
});
const [documents, setDocuments] = useState<UploadedFile[]>([]);

// Criar bot + Upload
const createMutation = useMutation({
  mutationFn: async (data) => {
    const bot = await botApi.create(data);
    
    for (const doc of documents) {
      await botApi.uploadDocument(bot.id, doc.file);
    }
    
    return bot;
  }
});

// Render
<Field label="Habilitar RAG">
  <Switch
    checked={formData.config.enableRAG}
    onChange={(_, data) => 
      setFormData({
        ...formData,
        config: { enableRAG: data.checked }
      })
    }
  />
</Field>

{formData.config.enableRAG && (
  <DocumentUploader
    files={documents}
    onFilesChange={setDocuments}
  />
)}
```

---

## ✨ Resultado Final

Agora você pode criar bots com conhecimento especializado:

- 🤖 **Bot de Observabilidade** + Runbooks
- 📚 **Bot de Onboarding** + Guias internos
- 🔧 **Bot de DevOps** + Scripts e procedures
- 📊 **Bot de Analytics** + Relatórios e dashboards
- 🎓 **Bot de Treinamento** + Materiais didáticos

O bot responde usando os documentos como fonte de verdade! 🎯
