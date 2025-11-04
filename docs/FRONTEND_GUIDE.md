# 🎨 Guia do Frontend - Teams Bot Automation

## 📋 Visão Geral

Frontend moderno construído com:
- **React 18** + **TypeScript** 
- **Vite** (bundler super rápido)
- **Fluent UI** (design system da Microsoft)
- **TanStack Query** (gerenciamento de dados)
- **Zustand** (state management)
- **React Router** (navegação)

---

## 🚀 Como Rodar o Frontend

### 1️⃣ Instalar Dependências

```powershell
# Na raiz do projeto
npm install
```

### 2️⃣ Iniciar a API (Terminal 1)

```powershell
# Certifique-se de que o MongoDB está rodando
# docker run -d -p 27017:27017 mongo:latest

# Configure o .env da API se ainda não fez
# packages/api/.env deve ter OPENAI_API_KEY

npm run dev:api
```

A API vai rodar em: **http://localhost:3001**

### 3️⃣ Iniciar o Frontend (Terminal 2)

```powershell
npm run dev:frontend
```

O frontend vai rodar em: **http://localhost:3000**

### 4️⃣ Abrir no Navegador

Acesse: **http://localhost:3000**

---

## 🎯 Funcionalidades Implementadas

### ✅ Galeria de Bots
- Visualizar todos os bots criados
- Cards com nome, descrição, tags e status
- Botões para conversar ou editar

### ✅ Criar Bot
- Formulário completo para criação
- Campos: nome, descrição, instruções, escopo, modelo
- Suporte a tags personalizadas
- Validação de campos obrigatórios

### ✅ Chat com Bot
- Interface de chat em tempo real
- Envio de mensagens
- Histórico de conversas
- Visual com avatares e bolhas de mensagem
- Loading state durante respostas

---

## 📁 Estrutura do Frontend

```
packages/frontend/
├── src/
│   ├── components/
│   │   └── Layout.tsx          # Layout principal com header e navegação
│   ├── pages/
│   │   ├── BotGallery.tsx      # Página de listagem de bots
│   │   ├── BotCreator.tsx      # Página de criação de bots
│   │   └── BotChat.tsx         # Página de chat com bot
│   ├── services/
│   │   ├── api.ts              # Configuração do Axios
│   │   └── botService.ts       # Funções para API (bots, chat)
│   ├── App.tsx                 # Componente raiz com rotas
│   ├── main.tsx                # Entry point
│   └── index.css               # Estilos globais
├── index.html                  # HTML base
├── vite.config.ts              # Configuração do Vite
├── package.json                # Dependências
└── .env                        # Variáveis de ambiente
```

---

## 🎨 Temas e Estilos

O projeto usa **Fluent UI** com o tema Microsoft:
- Design consistente com Teams
- Componentes acessíveis e responsivos
- Sistema de tokens (cores, espaçamentos)

### Customização de Cores

Edite `src/App.tsx` para mudar o tema:

```tsx
import { webDarkTheme } from '@fluentui/react-components';

// Trocar webLightTheme por webDarkTheme
<FluentProvider theme={webDarkTheme}>
```

---

## 🔧 Configuração

### Arquivo `.env`

```env
VITE_API_URL=http://localhost:3001/api/v1
VITE_AUTH_TOKEN=test-user-123
```

- **VITE_API_URL**: URL base da API
- **VITE_AUTH_TOKEN**: Token de autenticação temporário

---

## 🧪 Fluxo de Teste Completo

### 1. Criar um Bot

1. Clique em **"Criar Bot"** no header
2. Preencha o formulário:
   - **Nome**: Bot de Observabilidade
   - **Descrição**: Especialista em métricas e logs
   - **Instruções**: Você é um especialista em observabilidade...
   - **Escopo**: Pessoal
   - **Modelo**: GPT-4 Turbo
   - **Tags**: observability, monitoring, sre
3. Clique em **"Criar Bot"**

### 2. Ver na Galeria

1. Você será redirecionado para **"Meus Bots"**
2. Veja o card do bot criado
3. Observe o contador de conversas (0)

### 3. Conversar com o Bot

1. Clique em **"Conversar"** no card
2. Digite uma mensagem: "Explique o que é latência"
3. Clique em **"Enviar"**
4. Aguarde a resposta do bot
5. Continue a conversa normalmente

---

## 🛠️ Desenvolvimento

### Hot Reload

O Vite oferece **Hot Module Replacement (HMR)**:
- Edite qualquer arquivo `.tsx`
- As mudanças aparecem instantaneamente
- Sem recarregar a página completa

### Adicionar Nova Página

1. Crie o arquivo em `src/pages/MinhaPage.tsx`
2. Adicione a rota em `src/App.tsx`:

```tsx
import { MinhaPage } from './pages/MinhaPage';

// Dentro de <Routes>
<Route path="/minha-rota" element={<MinhaPage />} />
```

### Adicionar Novo Componente

1. Crie em `src/components/MeuComponente.tsx`
2. Use o hook `makeStyles` do Fluent UI:

```tsx
import { makeStyles, tokens } from '@fluentui/react-components';

const useStyles = makeStyles({
  root: {
    padding: '16px',
    backgroundColor: tokens.colorNeutralBackground1,
  },
});

export function MeuComponente() {
  const styles = useStyles();
  return <div className={styles.root}>Conteúdo</div>;
}
```

---

## 📊 State Management

### TanStack Query (React Query)

Usado para cache e sincronização de dados da API:

```tsx
// Buscar dados
const { data, isLoading } = useQuery({
  queryKey: ['bots'],
  queryFn: () => botApi.list(),
});

// Mutar dados
const mutation = useMutation({
  mutationFn: (input) => botApi.create(input),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['bots'] });
  },
});
```

### Zustand (Future)

Para state global complexo (usuário, configurações):

```tsx
// Será implementado quando necessário
```

---

## 🐛 Troubleshooting

### Porta 3000 já está em uso

```powershell
# Windows: matar processo na porta 3000
Get-Process -Id (Get-NetTCPConnection -LocalPort 3000).OwningProcess | Stop-Process
```

### API não responde (CORS)

Verifique se a API está rodando em `http://localhost:3001`:

```powershell
# Testar health da API
Invoke-RestMethod -Uri "http://localhost:3001/api/v1/health"
```

### Dependências não instaladas

```powershell
# Limpar e reinstalar
Remove-Item -Recurse -Force node_modules
Remove-Item package-lock.json
npm install
```

### Build não funciona

```powershell
# Build manual
cd packages/frontend
npm run build

# Verificar dist/
ls dist
```

---

## 🚀 Build para Produção

```powershell
# Build otimizado
npm run build --workspace=@teams-bot/frontend

# Preview do build
npm run preview --workspace=@teams-bot/frontend
```

Arquivos gerados em: `packages/frontend/dist/`

---

## 📦 Dependências Principais

| Pacote | Versão | Uso |
|--------|--------|-----|
| react | 18.2.0 | Framework UI |
| @fluentui/react-components | 9.47.0 | Componentes UI |
| @tanstack/react-query | 5.17.19 | Cache de dados |
| react-router-dom | 6.21.1 | Navegação |
| axios | 1.6.5 | Requisições HTTP |
| vite | 5.0.11 | Bundler |
| zustand | 4.4.7 | State management |

---

## 🎯 Próximos Passos

### Funcionalidades Pendentes

1. **Upload de Documentos**
   - Drag & drop de arquivos
   - Barra de progresso
   - Lista de documentos anexados

2. **Edição de Bots**
   - Formulário de edição
   - Histórico de versões
   - Delete com confirmação

3. **Gestão de Squads**
   - Criar e gerenciar squads
   - Atribuir bots a squads
   - Controle de permissões

4. **Azure AD Integration**
   - Login com Microsoft
   - Perfil do usuário
   - Logout

5. **Melhorias no Chat**
   - Suporte a markdown
   - Code highlighting
   - Anexar arquivos na conversa
   - Feedback (like/dislike)

---

## 💡 Dicas

- Use **Ctrl+Shift+P** no VS Code e digite "React" para snippets
- Instale a extensão **ES7+ React/Redux/React-Native snippets**
- Use **React DevTools** no Chrome para debug
- Inspecione Network tab para ver requisições à API

---

## 📚 Recursos

- [React Docs](https://react.dev)
- [Fluent UI](https://react.fluentui.dev)
- [TanStack Query](https://tanstack.com/query)
- [Vite Guide](https://vitejs.dev/guide)

---

## ✨ Enjoy!

Agora você tem um frontend completo e funcional! 🎉
