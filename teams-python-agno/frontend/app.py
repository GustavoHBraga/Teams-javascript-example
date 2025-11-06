"""
Streamlit Frontend - Teams Bot Automation
"""
import sys
from pathlib import Path

# Adiciona pasta raiz ao path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
import requests
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Teams Bot Automation",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Base URL
API_URL = "http://localhost:8000/api"


def main():
    """Aplicação principal"""
    
    # Sidebar
    with st.sidebar:
        st.title("🤖 Teams Bot")
        st.markdown("---")
        
        page = st.radio(
            "Navegação",
            ["🏠 Home", "➕ Criar Bot", "📚 Meus Bots", "💬 Chat", "📄 Documentos"]
        )
        
        st.markdown("---")
        st.caption("Powered by AgentOps")
    
    # Páginas
    if page == "🏠 Home":
        show_home()
    elif page == "➕ Criar Bot":
        show_create_bot()
    elif page == "📚 Meus Bots":
        show_bots_gallery()
    elif page == "💬 Chat":
        show_chat()
    elif page == "📄 Documentos":
        show_documents()


def show_home():
    """Página inicial"""
    st.title("🏠 Bem-vindo ao Teams Bot Automation")
    
    st.markdown("""
    ## 🎯 O que você pode fazer:
    
    - ✅ **Criar Bots** com instruções personalizadas
    - ✅ **Treinar com Documentos** (PDF, DOCX, TXT)
    - ✅ **Chatear com IA** usando RAG
    - ✅ **Monitorar** com AgentOps
    
    ### 🚀 Comece agora:
    1. Crie um bot na página "➕ Criar Bot"
    2. Faça upload de documentos
    3. Comece a conversar!
    """)
    
    # Estatísticas
    col1, col2, col3 = st.columns(3)
    
    try:
        # Busca estatísticas
        bots_response = requests.get(f"{API_URL}/bots")
        docs_response = requests.get(f"{API_URL}/documents")
        
        if bots_response.status_code == 200:
            bots_count = len(bots_response.json())
            col1.metric("🤖 Bots", bots_count)
        
        if docs_response.status_code == 200:
            docs_count = len(docs_response.json())
            col2.metric("📄 Documentos", docs_count)
        
        col3.metric("💬 Conversas", "-")
        
    except:
        st.warning("⚠️ Não foi possível carregar estatísticas. Verifique se a API está rodando.")


def show_create_bot():
    """Página de criação de bot"""
    st.title("➕ Criar Novo Bot")
    
    with st.form("create_bot_form"):
        name = st.text_input("Nome do Bot", placeholder="Assistente Python")
        description = st.text_area("Descrição", placeholder="Expert em Python e FastAPI")
        instructions = st.text_area(
            "Instruções do Bot",
            placeholder="Você é um especialista em Python...",
            height=200
        )
        enable_rag = st.checkbox("Habilitar RAG (Treinamento com Documentos)", value=True)
        
        submitted = st.form_submit_button("Criar Bot", use_container_width=True)
        
        if submitted:
            if not name or not description or not instructions:
                st.error("❌ Preencha todos os campos!")
                return
            
            # Cria bot
            try:
                response = requests.post(
                    f"{API_URL}/bots",
                    json={
                        "name": name,
                        "description": description,
                        "instructions": instructions,
                        "enable_rag": enable_rag
                    }
                )
                
                if response.status_code == 201:
                    st.success(f"✅ Bot '{name}' criado com sucesso!")
                    bot = response.json()
                    
                    # Mostra detalhes
                    st.json(bot)
                else:
                    st.error(f"❌ Erro ao criar bot: {response.text}")
                    
            except Exception as e:
                st.error(f"❌ Erro: {e}")


def show_bots_gallery():
    """Galeria de bots"""
    st.title("📚 Meus Bots")
    
    try:
        response = requests.get(f"{API_URL}/bots")
        
        if response.status_code == 200:
            bots = response.json()
            
            if not bots:
                st.info("Você ainda não tem bots. Crie um na página '➕ Criar Bot'")
                return
            
            # Grid de bots
            for bot in bots:
                with st.expander(f"🤖 {bot['name']}", expanded=False):
                    st.markdown(f"**Descrição:** {bot['description']}")
                    st.markdown(f"**RAG:** {'✅ Habilitado' if bot['enable_rag'] else '❌ Desabilitado'}")
                    st.markdown(f"**Criado:** {bot['created_at']}")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button(f"💬 Chat", key=f"chat_{bot['id']}"):
                            st.session_state.selected_bot = bot
                            st.rerun()
                    
                    with col2:
                        if st.button(f"🗑️ Deletar", key=f"delete_{bot['id']}"):
                            delete_response = requests.delete(f"{API_URL}/bots/{bot['id']}")
                            if delete_response.status_code == 204:
                                st.success("✅ Bot deletado!")
                                st.rerun()
        else:
            st.error("❌ Erro ao carregar bots")
            
    except Exception as e:
        st.error(f"❌ Erro: {e}")


def show_chat():
    """Interface de chat"""
    st.title("💬 Chat com Bot")
    
    # Seleciona bot
    try:
        response = requests.get(f"{API_URL}/bots")
        
        if response.status_code == 200:
            bots = response.json()
            
            if not bots:
                st.warning("⚠️ Você precisa criar um bot primeiro!")
                return
            
            # Select box
            bot_names = [f"{bot['name']} (ID: {bot['id'][:8]})" for bot in bots]
            selected_bot_name = st.selectbox("Selecione um bot:", bot_names)
            selected_bot = bots[bot_names.index(selected_bot_name)]
            
            st.markdown(f"**Descrição:** {selected_bot['description']}")
            st.markdown("---")
            
            # Histórico de mensagens
            if "messages" not in st.session_state:
                st.session_state.messages = []
            
            # Mostra mensagens
            for msg in st.session_state.messages:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])
                    if msg["role"] == "assistant" and msg.get("sources"):
                        st.caption(f"📚 Fontes: {', '.join(msg['sources'])}")
            
            # Input de mensagem
            if prompt := st.chat_input("Digite sua mensagem..."):
                # Adiciona mensagem do usuário
                st.session_state.messages.append({"role": "user", "content": prompt})
                
                with st.chat_message("user"):
                    st.markdown(prompt)
                
                # Chama API
                with st.spinner("Pensando..."):
                    try:
                        chat_response = requests.post(
                            f"{API_URL}/chat",
                            json={
                                "bot_id": selected_bot['id'],
                                "message": prompt
                            }
                        )
                        
                        if chat_response.status_code == 200:
                            data = chat_response.json()
                            
                            # Adiciona resposta do assistente
                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": data["response"],
                                "sources": data.get("sources", [])
                            })
                            
                            with st.chat_message("assistant"):
                                st.markdown(data["response"])
                                if data.get("sources"):
                                    st.caption(f"📚 Fontes: {', '.join(data['sources'])}")
                        else:
                            st.error(f"❌ Erro: {chat_response.text}")
                            
                    except Exception as e:
                        st.error(f"❌ Erro ao enviar mensagem: {e}")
        else:
            st.error("❌ Erro ao carregar bots")
            
    except Exception as e:
        st.error(f"❌ Erro: {e}")


def show_documents():
    """Gerenciamento de documentos"""
    st.title("📄 Documentos")
    
    # Upload de documento
    st.subheader("📤 Upload de Documento")
    
    try:
        # Seleciona bot
        response = requests.get(f"{API_URL}/bots")
        
        if response.status_code == 200:
            bots = response.json()
            
            if not bots:
                st.warning("⚠️ Crie um bot primeiro!")
                return
            
            bot_names = [f"{bot['name']}" for bot in bots]
            selected_bot_name = st.selectbox("Bot:", bot_names)
            selected_bot = bots[bot_names.index(selected_bot_name)]
            
            # Upload
            uploaded_file = st.file_uploader(
                "Escolha um arquivo",
                type=["pdf", "docx", "txt", "md"],
                help="Formatos: PDF, DOCX, TXT, MD"
            )
            
            if uploaded_file:
                if st.button("📤 Fazer Upload"):
                    with st.spinner("Fazendo upload..."):
                        try:
                            files = {"file": uploaded_file}
                            data = {"bot_id": selected_bot['id']}
                            
                            upload_response = requests.post(
                                f"{API_URL}/documents",
                                files=files,
                                data=data
                            )
                            
                            if upload_response.status_code == 201:
                                st.success("✅ Upload concluído! Processando documento...")
                                st.json(upload_response.json())
                            else:
                                st.error(f"❌ Erro: {upload_response.text}")
                                
                        except Exception as e:
                            st.error(f"❌ Erro: {e}")
            
            st.markdown("---")
            
            # Lista documentos
            st.subheader("📚 Documentos do Bot")
            
            docs_response = requests.get(f"{API_URL}/documents?bot_id={selected_bot['id']}")
            
            if docs_response.status_code == 200:
                docs = docs_response.json()
                
                if not docs:
                    st.info("Nenhum documento ainda")
                else:
                    for doc in docs:
                        status_icon = {
                            "processing": "⏳",
                            "completed": "✅",
                            "failed": "❌"
                        }.get(doc['status'], "❓")
                        
                        with st.expander(f"{status_icon} {doc['filename']}", expanded=False):
                            st.markdown(f"**Status:** {doc['status']}")
                            st.markdown(f"**Chunks:** {doc['chunk_count']}")
                            st.markdown(f"**Tamanho:** {doc['file_size']} bytes")
                            st.markdown(f"**Upload:** {doc['created_at']}")
                            
                            if st.button(f"🗑️ Deletar", key=f"del_{doc['id']}"):
                                del_response = requests.delete(f"{API_URL}/documents/{doc['id']}")
                                if del_response.status_code == 204:
                                    st.success("✅ Documento deletado!")
                                    st.rerun()
        else:
            st.error("❌ Erro ao carregar bots")
            
    except Exception as e:
        st.error(f"❌ Erro: {e}")


if __name__ == "__main__":
    main()
