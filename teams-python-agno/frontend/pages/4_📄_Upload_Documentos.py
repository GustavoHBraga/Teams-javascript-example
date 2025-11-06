"""
Upload de Documentos - Gerenciamento de documentos para RAG
"""
import streamlit as st
import requests
import os
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Upload de Documentos",
    page_icon="📄",
    layout="wide"
)

# API URL
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.title("📄 Upload de Documentos para RAG")
st.markdown("Faça upload de documentos para treinar seus bots com conhecimento específico")

# Sidebar - Seleção de Bot
with st.sidebar:
    st.header("🤖 Selecionar Bot")
    
    # Carregar bots com RAG ativo
    try:
        response = requests.get(f"{API_URL}/bots")
        all_bots = response.json()
        
        # Filtrar apenas bots com RAG
        rag_bots = [b for b in all_bots if b.get("enable_rag", False)]
        
        if rag_bots:
            # Se há bot selecionado no session_state
            if "selected_bot" in st.session_state:
                default_bot = st.session_state.selected_bot
                default_index = next(
                    (i for i, b in enumerate(rag_bots) if b["id"] == default_bot.get("id")),
                    0
                )
            else:
                default_index = 0
            
            # Selectbox com bots
            bot_names = [b["name"] for b in rag_bots]
            selected_name = st.selectbox(
                "Bot:",
                options=bot_names,
                index=default_index,
                label_visibility="collapsed"
            )
            
            # Encontrar bot selecionado
            selected_bot = next(b for b in rag_bots if b["name"] == selected_name)
            
            # Info do bot
            st.divider()
            st.markdown(f"**{selected_bot['name']}**")
            st.caption(selected_bot.get("description", "Sem descrição"))
            
            # Estatísticas de documentos
            try:
                docs_response = requests.get(f"{API_URL}/documents/{selected_bot['id']}")
                documents = docs_response.json() if docs_response.ok else []
                
                st.metric("📚 Documentos", len(documents))
                
                total_chunks = sum(d.get("chunk_count", 0) for d in documents)
                st.metric("🧩 Chunks", total_chunks)
            except:
                documents = []
        
        else:
            st.warning("Nenhum bot com RAG disponível")
            if st.button("➕ Criar Bot com RAG", use_container_width=True):
                st.switch_page("pages/2_🎨_Criar_Bot.py")
            selected_bot = None
            documents = []
    
    except Exception as e:
        st.error(f"Erro ao carregar bots: {e}")
        selected_bot = None
        documents = []

# Área principal
if selected_bot:
    # Tabs para Upload e Gerenciar
    tab_upload, tab_manage = st.tabs(["⬆️ Upload", "📋 Gerenciar"])
    
    # Tab Upload
    with tab_upload:
        st.subheader("⬆️ Fazer Upload de Documentos")
        
        # Info sobre formatos
        st.info("""
        📋 **Formatos suportados:** PDF, DOCX, TXT, MD
        
        📏 **Tamanho máximo:** 10 MB por arquivo
        
        🧠 **Processamento:** Os documentos serão divididos em chunks e convertidos em embeddings para busca semântica.
        """)
        
        # Upload de arquivo
        uploaded_files = st.file_uploader(
            "Escolha os arquivos",
            type=["pdf", "docx", "txt", "md"],
            accept_multiple_files=True,
            help="Selecione um ou mais documentos para fazer upload"
        )
        
        if uploaded_files:
            st.write(f"📁 {len(uploaded_files)} arquivo(s) selecionado(s)")
            
            # Mostrar preview dos arquivos
            for file in uploaded_files:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.text(f"📄 {file.name}")
                with col2:
                    size_mb = file.size / (1024 * 1024)
                    st.text(f"{size_mb:.2f} MB")
                with col3:
                    st.text(file.type)
            
            # Botão de upload
            if st.button("⬆️ Fazer Upload", type="primary", use_container_width=True):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                successful_uploads = 0
                
                for idx, file in enumerate(uploaded_files):
                    try:
                        status_text.text(f"Uploading {file.name}...")
                        
                        # Preparar arquivo para envio
                        files = {"file": (file.name, file, file.type)}
                        
                        # Fazer upload
                        response = requests.post(
                            f"{API_URL}/documents/{selected_bot['id']}",
                            files=files
                        )
                        response.raise_for_status()
                        
                        successful_uploads += 1
                        
                    except Exception as e:
                        st.error(f"❌ Erro ao fazer upload de {file.name}: {str(e)}")
                    
                    # Atualizar barra de progresso
                    progress_bar.progress((idx + 1) / len(uploaded_files))
                
                # Mensagem final
                if successful_uploads > 0:
                    st.success(f"✅ {successful_uploads} arquivo(s) enviado(s) com sucesso!")
                    st.balloons()
                    status_text.text("Upload concluído!")
                    
                    # Limpar cache e recarregar
                    st.rerun()
                else:
                    status_text.text("Upload falhou")
    
    # Tab Gerenciar
    with tab_manage:
        st.subheader("📋 Documentos do Bot")
        
        if not documents:
            st.info("📭 Nenhum documento enviado ainda. Faça upload na aba 'Upload'!")
        else:
            # Filtros
            col1, col2 = st.columns([3, 1])
            with col1:
                search_doc = st.text_input("🔍 Buscar documento", placeholder="Digite o nome...")
            with col2:
                filter_status = st.selectbox("Status", ["Todos", "Completo", "Processando", "Erro"])
            
            # Filtrar documentos
            filtered_docs = documents
            if search_doc:
                filtered_docs = [d for d in filtered_docs if search_doc.lower() in d["filename"].lower()]
            if filter_status != "Todos":
                filtered_docs = [d for d in filtered_docs if d["status"].lower() == filter_status.lower()]
            
            st.write(f"📊 {len(filtered_docs)} documento(s) encontrado(s)")
            
            # Listar documentos
            for doc in filtered_docs:
                with st.container(border=True):
                    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                    
                    with col1:
                        st.markdown(f"**📄 {doc['filename']}**")
                        st.caption(f"ID: {doc['id'][:8]}...")
                    
                    with col2:
                        # Status badge
                        status = doc.get("status", "unknown")
                        if status == "completed":
                            st.success("✅ Completo")
                        elif status == "processing":
                            st.info("⏳ Processando")
                        elif status == "failed":
                            st.error("❌ Erro")
                        else:
                            st.warning(f"⚠️ {status}")
                    
                    with col3:
                        # Estatísticas
                        size_mb = doc.get("file_size", 0) / (1024 * 1024)
                        st.metric("Tamanho", f"{size_mb:.1f} MB", label_visibility="collapsed")
                        st.caption(f"{doc.get('chunk_count', 0)} chunks")
                    
                    with col4:
                        # Botão deletar
                        if st.button("🗑️", key=f"del_{doc['id']}", help="Deletar documento"):
                            try:
                                del_response = requests.delete(f"{API_URL}/documents/{doc['id']}")
                                del_response.raise_for_status()
                                st.success("Documento deletado!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Erro ao deletar: {e}")
                    
                    # Detalhes expandíveis
                    with st.expander("ℹ️ Detalhes"):
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.text(f"Tipo: {doc.get('content_type', 'N/A')}")
                            st.text(f"Chunks: {doc.get('chunk_count', 0)}")
                        with col_b:
                            uploaded_at = doc.get('created_at', 'N/A')
                            st.text(f"Upload: {uploaded_at[:19] if uploaded_at != 'N/A' else 'N/A'}")
            
            # Botões de ação
            st.divider()
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🔄 Atualizar Lista", use_container_width=True):
                    st.rerun()
            
            with col2:
                if st.button("🗑️ Deletar Todos", use_container_width=True):
                    if st.session_state.get("confirm_delete_all", False):
                        # Deletar todos
                        for doc in documents:
                            try:
                                requests.delete(f"{API_URL}/documents/{doc['id']}")
                            except:
                                pass
                        st.success("Todos os documentos foram deletados!")
                        st.session_state.confirm_delete_all = False
                        st.rerun()
                    else:
                        st.session_state.confirm_delete_all = True
                        st.warning("⚠️ Clique novamente para confirmar exclusão de TODOS os documentos")

else:
    # Nenhum bot com RAG
    st.info("👆 Selecione um bot com RAG ativo ou crie um novo")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Criar Bot com RAG", type="primary", use_container_width=True):
            st.switch_page("pages/2_🎨_Criar_Bot.py")
    
    with col2:
        if st.button("🤖 Ver Bots", use_container_width=True):
            st.switch_page("pages/1_🤖_Galeria_de_Bots.py")

# Info no rodapé
st.divider()
with st.expander("❓ Como funciona o RAG?"):
    st.markdown("""
    ### 🧠 Retrieval Augmented Generation (RAG)
    
    **O que é:**
    RAG é uma técnica que permite que modelos de IA usem documentos externos como contexto.
    
    **Como funciona:**
    1. 📄 Você faz upload de documentos (PDFs, DOCs, etc.)
    2. ✂️ Os documentos são divididos em pequenos chunks
    3. 🔢 Cada chunk é convertido em embeddings (vetores numéricos)
    4. 💾 Os embeddings são armazenados no ChromaDB
    5. 💬 Quando você faz uma pergunta, o sistema busca os chunks mais relevantes
    6. 🤖 O bot usa esses chunks como contexto para responder
    
    **Benefícios:**
    - ✅ Respostas mais precisas e contextualizadas
    - ✅ Conhecimento específico do seu domínio
    - ✅ Reduz alucinações do modelo
    - ✅ Permite citação de fontes
    """)
