"""
Chat - Interface de conversa com os bots
"""
import streamlit as st
import requests
import os
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Chat com Bot",
    page_icon="💬",
    layout="wide"
)

# API URL
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.title("💬 Chat com Bot")

# Inicializar session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = None

# Sidebar - Seleção de Bot
with st.sidebar:
    st.header("🤖 Selecionar Bot")
    
    # Carregar bots disponíveis
    try:
        response = requests.get(f"{API_URL}/bots")
        bots = response.json()
        
        # Se há bot selecionado no session_state
        if "selected_bot" in st.session_state:
            default_bot = st.session_state.selected_bot
            default_index = next(
                (i for i, b in enumerate(bots) if b["id"] == default_bot.get("id")),
                0
            )
        else:
            default_index = 0
        
        # Selectbox com bots
        if bots:
            bot_options = [f"{b['name']} {'🧠' if b.get('enable_rag') else '💬'}" for b in bots]
            selected_option = st.selectbox(
                "Escolha um bot:",
                options=bot_options,
                index=default_index,
                label_visibility="collapsed"
            )
            
            # Encontrar bot selecionado
            selected_index = bot_options.index(selected_option)
            selected_bot = bots[selected_index]
            
            # Mostrar info do bot
            st.divider()
            st.subheader(selected_bot["name"])
            st.markdown(f"_{selected_bot.get('description', 'Sem descrição')}_")
            
            with st.expander("ℹ️ Instruções do Bot"):
                st.text(selected_bot.get("instructions", "N/A"))
            
            # Badge RAG
            if selected_bot.get("enable_rag"):
                st.success("🧠 RAG Ativo - Usando documentos")
            else:
                st.info("💬 Chat Básico")
            
            # Botão para nova conversa
            if st.button("🔄 Nova Conversa", use_container_width=True):
                st.session_state.messages = []
                st.session_state.session_id = None
                st.rerun()
            
            # Botão para ver documentos (se RAG)
            if selected_bot.get("enable_rag"):
                if st.button("📄 Ver Documentos", use_container_width=True):
                    st.session_state.selected_bot = selected_bot
                    st.switch_page("pages/4_📄_Upload_Documentos.py")
        
        else:
            st.warning("Nenhum bot disponível. Crie um primeiro!")
            if st.button("➕ Criar Bot", use_container_width=True):
                st.switch_page("pages/2_🎨_Criar_Bot.py")
            selected_bot = None
    
    except Exception as e:
        st.error(f"Erro ao carregar bots: {e}")
        selected_bot = None

# Área principal - Chat
if selected_bot:
    # Exibir mensagens
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
                # Mostrar fontes (se RAG)
                if message.get("sources"):
                    with st.expander("📚 Fontes"):
                        for source in message["sources"]:
                            st.markdown(f"- {source}")
    
    # Input de mensagem
    if prompt := st.chat_input("Digite sua mensagem..."):
        # Adicionar mensagem do usuário
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
            "timestamp": datetime.now().isoformat()
        })
        
        # Exibir mensagem do usuário
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Enviar para API e receber resposta
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                try:
                    payload = {
                        "bot_id": selected_bot["id"],
                        "message": prompt,
                        "session_id": st.session_state.session_id
                    }
                    
                    response = requests.post(f"{API_URL}/chat", json=payload)
                    response.raise_for_status()
                    
                    data = response.json()
                    
                    # Atualizar session_id
                    if not st.session_state.session_id:
                        st.session_state.session_id = data.get("session_id")
                    
                    # Mostrar resposta
                    st.markdown(data["response"])
                    
                    # Mostrar fontes (se houver)
                    if data.get("sources"):
                        with st.expander("📚 Fontes usadas"):
                            for source in data["sources"]:
                                st.markdown(f"- {source}")
                    
                    # Adicionar à história
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": data["response"],
                        "sources": data.get("sources", []),
                        "timestamp": datetime.now().isoformat()
                    })
                
                except requests.exceptions.HTTPError as e:
                    st.error(f"❌ Erro na API: {e.response.text}")
                except Exception as e:
                    st.error(f"❌ Erro inesperado: {str(e)}")
    
    # Estatísticas da conversa
    if st.session_state.messages:
        st.divider()
        col1, col2, col3 = st.columns(3)
        
        with col1:
            user_msgs = len([m for m in st.session_state.messages if m["role"] == "user"])
            st.metric("Suas mensagens", user_msgs)
        
        with col2:
            bot_msgs = len([m for m in st.session_state.messages if m["role"] == "assistant"])
            st.metric("Respostas do bot", bot_msgs)
        
        with col3:
            if st.button("📥 Exportar Chat"):
                # Criar texto do chat
                chat_text = f"# Chat com {selected_bot['name']}\n\n"
                for msg in st.session_state.messages:
                    role = "Você" if msg["role"] == "user" else selected_bot["name"]
                    chat_text += f"**{role}:** {msg['content']}\n\n"
                
                st.download_button(
                    label="💾 Baixar",
                    data=chat_text,
                    file_name=f"chat_{selected_bot['name']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                    mime="text/markdown"
                )

else:
    # Nenhum bot disponível
    st.info("👆 Selecione ou crie um bot para começar a conversar")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Criar Novo Bot", type="primary", use_container_width=True):
            st.switch_page("pages/2_🎨_Criar_Bot.py")
    
    with col2:
        if st.button("🤖 Ver Bots", use_container_width=True):
            st.switch_page("pages/1_🤖_Galeria_de_Bots.py")
