"""
Criar Bot - Formulário para criar novos bots
"""
import streamlit as st
import requests
import os

# Configuração da página
st.set_page_config(
    page_title="Criar Bot",
    page_icon="🎨",
    layout="wide"
)

# API URL
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.title("🎨 Criar Novo Bot")
st.markdown("Crie um agente de IA personalizado com instruções e documentos")

# Formulário de criação
with st.form("create_bot_form"):
    st.subheader("📝 Informações Básicas")
    
    # Nome e Descrição
    name = st.text_input(
        "Nome do Bot *",
        placeholder="Ex: Assistente de Vendas",
        help="Escolha um nome único e descritivo"
    )
    
    description = st.text_area(
        "Descrição",
        placeholder="Ex: Bot especializado em responder perguntas sobre produtos",
        help="Descreva o propósito do bot",
        height=100
    )
    
    # Instruções
    st.divider()
    st.subheader("🧠 Instruções para o Bot")
    
    instructions = st.text_area(
        "Instruções *",
        placeholder="""Você é um assistente especializado em [área].
Seu objetivo é ajudar os usuários a [objetivo].

Regras:
- Seja sempre educado e profissional
- Se não souber a resposta, seja honesto
- Use informações dos documentos fornecidos quando disponível""",
        help="Defina a personalidade e comportamento do bot",
        height=200
    )
    
    # Exemplos de instruções
    with st.expander("💡 Ver exemplos de instruções"):
        st.markdown("""
        **Assistente de Suporte:**
        ```
        Você é um assistente de suporte técnico amigável.
        Ajude os usuários a resolver problemas com produtos.
        Seja paciente e forneça soluções passo a passo.
        ```
        
        **Vendedor Virtual:**
        ```
        Você é um vendedor especialista.
        Recomende produtos baseado nas necessidades do cliente.
        Destaque benefícios e responda objeções com empatia.
        ```
        
        **Professor Virtual:**
        ```
        Você é um professor paciente e didático.
        Explique conceitos complexos de forma simples.
        Use exemplos práticos e analogias.
        ```
        """)
    
    # RAG Configuration
    st.divider()
    st.subheader("🧬 Configuração RAG (Retrieval Augmented Generation)")
    
    enable_rag = st.checkbox(
        "Ativar RAG",
        value=True,
        help="Permite que o bot use documentos como contexto"
    )
    
    if enable_rag:
        st.info("""
        ℹ️ **O que é RAG?**
        
        RAG permite que o bot use documentos como fonte de conhecimento.
        Após criar o bot, você poderá fazer upload de PDFs, DOCs, e outros arquivos.
        O bot usará essas informações para dar respostas mais precisas.
        """)
        
        # Upload de documentos (após criar o bot)
        st.markdown("📄 Você poderá fazer upload de documentos após criar o bot")
    
    # Botão de submit
    st.divider()
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col2:
        cancel = st.form_submit_button("❌ Cancelar", use_container_width=True)
    
    with col3:
        submit = st.form_submit_button("✅ Criar Bot", type="primary", use_container_width=True)

# Processar formulário
if submit:
    # Validação
    errors = []
    
    if not name or len(name.strip()) < 3:
        errors.append("Nome deve ter pelo menos 3 caracteres")
    
    if not instructions or len(instructions.strip()) < 10:
        errors.append("Instruções devem ter pelo menos 10 caracteres")
    
    if errors:
        for error in errors:
            st.error(f"❌ {error}")
    else:
        # Criar bot via API
        try:
            with st.spinner("Criando bot..."):
                payload = {
                    "name": name.strip(),
                    "description": description.strip() if description else "",
                    "instructions": instructions.strip(),
                    "enable_rag": enable_rag
                }
                
                response = requests.post(f"{API_URL}/bots", json=payload)
                response.raise_for_status()
                
                bot_data = response.json()
                
                st.success(f"✅ Bot '{name}' criado com sucesso!")
                st.balloons()
                
                # Mostrar próximos passos
                st.info(f"""
                🎉 **Próximos passos:**
                
                1. ✅ Bot criado (ID: {bot_data.get('id', 'N/A')})
                2. 📄 Faça upload de documentos para treinar o bot (se RAG ativo)
                3. 💬 Comece a conversar com seu bot!
                """)
                
                # Botões de ação
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("📄 Upload Documentos", type="primary", use_container_width=True):
                        st.session_state.selected_bot = bot_data
                        st.switch_page("pages/4_📄_Upload_Documentos.py")
                
                with col2:
                    if st.button("💬 Conversar Agora", use_container_width=True):
                        st.session_state.selected_bot = bot_data
                        st.switch_page("pages/3_💬_Chat.py")
        
        except requests.exceptions.HTTPError as e:
            st.error(f"❌ Erro ao criar bot: {e.response.text}")
        except Exception as e:
            st.error(f"❌ Erro inesperado: {str(e)}")

if cancel:
    st.switch_page("pages/1_🤖_Galeria_de_Bots.py")

# Dicas sidebar
with st.sidebar:
    st.header("💡 Dicas")
    
    st.markdown("""
    ### Nome do Bot
    - Use nomes descritivos
    - Evite caracteres especiais
    - Seja único e memorável
    
    ### Instruções
    - Seja específico sobre o comportamento
    - Defina limites claros
    - Use exemplos quando possível
    
    ### RAG
    - Ideal para bots especializados
    - Requer documentos de treinamento
    - Melhora precisão das respostas
    """)
    
    st.divider()
    
    st.markdown("### 📚 Recursos")
    st.markdown("""
    - [Guia de Instruções](https://docs.openai.com/guides/prompt-engineering)
    - [Boas Práticas RAG](https://docs.openai.com/guides/rag)
    - [Exemplos de Bots](https://examples.openai.com)
    """)
