"""
LLM Adapter - Suporta Azure OpenAI e OpenAI padrão
Adaptador genérico e dinâmico para diferentes provedores
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Union
from openai import AsyncAzureOpenAI, AsyncOpenAI
from shared.config import Settings


class BaseLLMAdapter(ABC):
    """Interface base para adaptadores LLM"""
    
    @abstractmethod
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> Dict:
        """Gera resposta de chat"""
        pass
    
    @abstractmethod
    async def generate_embedding(self, text: str) -> List[float]:
        """Gera embedding para um texto"""
        pass
    
    @abstractmethod
    async def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Gera embeddings em batch"""
        pass


class AzureOpenAIAdapter(BaseLLMAdapter):
    """Adaptador para Azure OpenAI (Corporativo)"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.client = AsyncAzureOpenAI(
            api_key=settings.azure_openai_api_key,
            api_version=settings.azure_openai_api_version,
            azure_endpoint=settings.azure_openai_endpoint
        )
        self.chat_deployment = settings.azure_chat_deployment
        self.embedding_deployment = settings.azure_embedding_deployment
        print(f"✅ Azure OpenAI Adapter inicializado")
        print(f"   Endpoint: {settings.azure_openai_endpoint}")
        print(f"   Chat Model: {self.chat_deployment}")
        print(f"   Embedding Model: {self.embedding_deployment}")
    
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> Dict:
        """Gera resposta usando Azure OpenAI"""
        try:
            response = await self.client.chat.completions.create(
                model=self.chat_deployment,  # Nome do deployment no Azure
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            
            return {
                "content": response.choices[0].message.content,
                "model": self.chat_deployment,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
                    "completion_tokens": response.usage.completion_tokens if response.usage else 0,
                    "total_tokens": response.usage.total_tokens if response.usage else 0
                },
                "finish_reason": response.choices[0].finish_reason
            }
        except Exception as e:
            print(f"❌ Erro ao chamar Azure OpenAI: {e}")
            raise
    
    async def generate_embedding(self, text: str) -> List[float]:
        """Gera embedding usando Azure OpenAI"""
        try:
            response = await self.client.embeddings.create(
                model=self.embedding_deployment,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"❌ Erro ao gerar embedding: {e}")
            raise
    
    async def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Gera embeddings em batch"""
        # Azure OpenAI suporta até 16 inputs por request
        batch_size = 16
        all_embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            try:
                response = await self.client.embeddings.create(
                    model=self.embedding_deployment,
                    input=batch
                )
                embeddings = [item.embedding for item in response.data]
                all_embeddings.extend(embeddings)
            except Exception as e:
                print(f"❌ Erro no batch {i//batch_size + 1}: {e}")
                raise
        
        return all_embeddings


class OpenAIAdapter(BaseLLMAdapter):
    """Adaptador para OpenAI padrão (Fallback)"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.chat_model = settings.openai_chat_model
        self.embedding_model = settings.openai_embedding_model
        print(f"✅ OpenAI Adapter inicializado")
        print(f"   Chat Model: {self.chat_model}")
        print(f"   Embedding Model: {self.embedding_model}")
    
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> Dict:
        """Gera resposta usando OpenAI padrão"""
        try:
            response = await self.client.chat.completions.create(
                model=self.chat_model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            
            return {
                "content": response.choices[0].message.content,
                "model": self.chat_model,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
                    "completion_tokens": response.usage.completion_tokens if response.usage else 0,
                    "total_tokens": response.usage.total_tokens if response.usage else 0
                },
                "finish_reason": response.choices[0].finish_reason
            }
        except Exception as e:
            print(f"❌ Erro ao chamar OpenAI: {e}")
            raise
    
    async def generate_embedding(self, text: str) -> List[float]:
        """Gera embedding usando OpenAI"""
        try:
            response = await self.client.embeddings.create(
                model=self.embedding_model,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"❌ Erro ao gerar embedding: {e}")
            raise
    
    async def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Gera embeddings em batch"""
        # OpenAI suporta até 2048 inputs por request
        batch_size = 100
        all_embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            try:
                response = await self.client.embeddings.create(
                    model=self.embedding_model,
                    input=batch
                )
                embeddings = [item.embedding for item in response.data]
                all_embeddings.extend(embeddings)
            except Exception as e:
                print(f"❌ Erro no batch {i//batch_size + 1}: {e}")
                raise
        
        return all_embeddings


class LLMAdapterFactory:
    """Factory para criar o adaptador correto"""
    
    @staticmethod
    def create_adapter(settings: Settings) -> BaseLLMAdapter:
        """Cria adaptador baseado na configuração"""
        if settings.use_azure:
            return AzureOpenAIAdapter(settings)
        else:
            return OpenAIAdapter(settings)


# Instância global (lazy loaded)
_llm_adapter: Optional[BaseLLMAdapter] = None


def get_llm_adapter(settings: Settings = None) -> BaseLLMAdapter:
    """Obtém instância do adaptador LLM"""
    global _llm_adapter
    
    if _llm_adapter is None:
        if settings is None:
            from shared.config import settings as default_settings
            settings = default_settings
        _llm_adapter = LLMAdapterFactory.create_adapter(settings)
    
    return _llm_adapter
