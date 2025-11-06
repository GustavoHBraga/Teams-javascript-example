"""
Chat Agent with AgentOps Integration
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from typing import List, Dict, Optional
import agentops
from openai import AsyncOpenAI
from shared.config import settings
from app.services.rag_service import rag_service


class ChatAgent:
    """Agente de chat com integração AgentOps"""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        print("✅ Chat Agent inicializado")
    
    @agentops.record_action("chat_with_rag")
    async def chat_with_rag(
        self,
        bot_id: str,
        bot_instructions: str,
        user_message: str,
        enable_rag: bool = True
    ) -> Dict:
        """
        Chat com RAG habilitado
        AgentOps rastreia automaticamente esta ação
        """
        
        # 1. Busca contexto relevante (se RAG habilitado)
        context_docs = []
        if enable_rag:
            context_docs = await rag_service.search_relevant_documents(
                bot_id=bot_id,
                query=user_message
            )
        
        # 2. Monta prompt com contexto
        system_prompt = self._build_system_prompt(
            bot_instructions,
            context_docs
        )
        
        # 3. Chama OpenAI (AgentOps rastreia automaticamente)
        response = await self.client.chat.completions.create(
            model=settings.chat_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        # 4. Extrai resposta
        assistant_message = response.choices[0].message.content
        
        # 5. Prepara resultado
        result = {
            "response": assistant_message,
            "sources": [doc["source"] for doc in context_docs],
            "context_used": len(context_docs) > 0,
            "model": settings.chat_model,
            "tokens_used": response.usage.total_tokens if response.usage else 0
        }
        
        return result
    
    def _build_system_prompt(
        self,
        bot_instructions: str,
        context_docs: List[Dict]
    ) -> str:
        """Monta system prompt com contexto RAG"""
        
        prompt = f"{bot_instructions}\n\n"
        
        if context_docs:
            prompt += "## Contexto Relevante dos Documentos:\n\n"
            
            for i, doc in enumerate(context_docs, 1):
                source = doc.get("source", "Unknown")
                content = doc.get("content", "")
                similarity = doc.get("similarity", 0)
                
                prompt += f"### Documento {i} (Similaridade: {similarity:.2%}):\n"
                prompt += f"**Fonte:** {source}\n"
                prompt += f"**Conteúdo:**\n{content}\n\n"
            
            prompt += "---\n\n"
            prompt += "Use as informações acima para responder a pergunta do usuário. "
            prompt += "Se a informação não estiver nos documentos, indique isso claramente.\n"
        
        return prompt
    
    @agentops.record_action("simple_chat")
    async def simple_chat(
        self,
        bot_instructions: str,
        user_message: str
    ) -> Dict:
        """Chat simples sem RAG"""
        
        response = await self.client.chat.completions.create(
            model=settings.chat_model,
            messages=[
                {"role": "system", "content": bot_instructions},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        assistant_message = response.choices[0].message.content
        
        return {
            "response": assistant_message,
            "sources": [],
            "context_used": False,
            "model": settings.chat_model,
            "tokens_used": response.usage.total_tokens if response.usage else 0
        }


# Instância global
chat_agent = ChatAgent()
