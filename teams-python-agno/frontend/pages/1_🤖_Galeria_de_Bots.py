"""
Galeria de Bots - Lista todos os bots criados
"""
import streamlit as st
import requests
import os

# Configuração da página
st.set_page_config(
    page_title="Galeria de Bots",
    page_icon="🤖",
    layout="wide"
)

# API URL
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.title("🤖 Galeria de Bots")
st.markdown("Veja todos os bots criados e gerencie-os")

# Função para carregar bots
@st.cache_data(ttl=10)
def load_bots():
    """Carrega lista de bots da API"""
    try:
        response = requests.get(f"{API_URL}/bots")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Erro ao carregar bots: {e}")
        return []

# Função para deletar bot
def delete_bot(bot_id):
    """Deleta um bot"""
    try:
        response = requests.delete(f"{API_URL}/bots/{bot_id}")
        response.raise_for_status()
        st.success("Bot deletado com sucesso!")
        st.cache_data.clear()
        st.rerun()
    except Exception as e:
        st.error(f"Erro ao deletar bot: {e}")

# Carregar bots
bots = load_bots()

# Filtros
col1, col2 = st.columns([3, 1])
with col1:
    search = st.text_input("🔍 Buscar bot", placeholder="Digite o nome do bot...")
with col2:
    filter_rag = st.selectbox("Filtrar por RAG", ["Todos", "Com RAG", "Sem RAG"])

# Filtrar bots
filtered_bots = bots
if search:
    filtered_bots = [b for b in filtered_bots if search.lower() in b["name"].lower()]
if filter_rag == "Com RAG":
    filtered_bots = [b for b in filtered_bots if b.get("enable_rag", False)]
elif filter_rag == "Sem RAG":
    filtered_bots = [b for b in filtered_bots if not b.get("enable_rag", False)]

# Exibir estatísticas
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total de Bots", len(bots))
with col2:
    rag_bots = len([b for b in bots if b.get("enable_rag", False)])
    st.metric("Bots com RAG", rag_bots)
with col3:
    active_bots = len([b for b in bots if b.get("is_active", True)])
    st.metric("Bots Ativos", active_bots)
with col4:
    st.metric("Resultados", len(filtered_bots))

st.divider()

# Exibir bots em cards
if not filtered_bots:
    st.info("📭 Nenhum bot encontrado. Crie seu primeiro bot!")
else:
    # Grid de 3 colunas
    cols = st.columns(3)
    
    for idx, bot in enumerate(filtered_bots):
        with cols[idx % 3]:
            with st.container(border=True):
                # Cabeçalho do card
                st.subheader(f"🤖 {bot['name']}")
                
                # Status badges
                col_badge1, col_badge2 = st.columns(2)
                with col_badge1:
                    if bot.get("enable_rag", False):
                        st.markdown("🧠 **RAG Ativo**")
                    else:
                        st.markdown("💬 **Chat Básico**")
                
                with col_badge2:
                    if bot.get("is_active", True):
                        st.markdown("✅ **Ativo**")
                    else:
                        st.markdown("⏸️ **Inativo**")
                
                # Descrição
                st.markdown(f"_{bot.get('description', 'Sem descrição')}_")
                
                # Informações adicionais
                with st.expander("📋 Detalhes"):
                    st.text(f"ID: {bot['id']}")
                    st.text(f"Criado em: {bot.get('created_at', 'N/A')}")
                    st.markdown("**Instruções:**")
                    st.text(bot.get('instructions', 'N/A')[:100] + "...")
                
                # Ações
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("💬 Chat", key=f"chat_{bot['id']}", use_container_width=True):
                        st.session_state.selected_bot = bot
                        st.switch_page("pages/3_💬_Chat.py")
                
                with col2:
                    if st.button("✏️ Editar", key=f"edit_{bot['id']}", use_container_width=True):
                        st.info("Em breve: Editar bot")
                
                with col3:
                    if st.button("🗑️ Deletar", key=f"del_{bot['id']}", use_container_width=True):
                        if st.session_state.get(f"confirm_del_{bot['id']}", False):
                            delete_bot(bot['id'])
                        else:
                            st.session_state[f"confirm_del_{bot['id']}"] = True
                            st.warning("Clique novamente para confirmar")
                            st.rerun()

# Botão para criar novo bot
st.divider()
if st.button("➕ Criar Novo Bot", type="primary", use_container_width=True):
    st.switch_page("pages/2_🎨_Criar_Bot.py")

# Refresh button
if st.button("🔄 Atualizar Lista"):
    st.cache_data.clear()
    st.rerun()
