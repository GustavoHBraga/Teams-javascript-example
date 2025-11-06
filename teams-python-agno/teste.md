🚀 Como usar AGORA:
Passo 1: Instalar dependências
# Backend
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install fastapi uvicorn sqlalchemy aiosqlite openai langchain chromadb agentops python-dotenv pydantic

# Frontend  
cd ../frontend
python -m venv venv
.\venv\Scripts\activate
pip install streamlit requests python-dotenv

Passo 2: Configurar .env
Crie backend/.env:
OPENAI_API_KEY=sk-your-key-here
AGENTOPS_API_KEY=your-key-here
DATABASE_TYPE=sqlite
DATABASE_URL=sqlite+aiosqlite:///./data/teams_bots.db

Passo 3: Iniciar
# Terminal 1 - Backend
cd backend
.\venv\Scripts\activate
uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd frontend
.\venv\Scripts\activate
streamlit run app.py

Passo 4: Acessar
Frontend: http://localhost:8501
Backend API: http://localhost:8000
Docs: http://localhost:8000/docs
💾 Migração de Database:
SQLite → PostgreSQL:
DATABASE_TYPE=postgresql
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/teams_bots

SQLite → MongoDB:
DATABASE_TYPE=mongodb
DATABASE_URL=mongodb://localhost:27017
O código já está preparado! Só trocar o .env 🚀

📁 Arquivos Criados:
🎯 Próximos Passos:
Testar agora: Rode .\start-all.ps1 (se o script existir)
Criar bots: Use a interface web
Upload docs: Treine os bots com documentos
Conversar: Chat com os bots treinados
Migrar DB: Quando precisar de produção
