import json
from src.genai.core.connectors.ai_provider import AIProvider
from src.prompts.prompt_templates import prompts
from src.genai.config.prompts import PromptManager
from src.genai.config.settings import AppConfig
from src.genai.core.connectors.vector_store import VectorStore
from src.genai.rag.retriever import Retriever
from .base import Chatbot
from .standard import StandardBot
from .rag import RAGBot

class ChatbotFactory:
    @staticmethod
    def create(bot_type: str, config : AppConfig) -> Chatbot:
        if bot_type == "standard":
            return StandardBot(config)
        elif bot_type == "rag":
            return RAGBot(
                config=config, 
                retriever=Retriever(VectorStore(config) ),
                prompt_manager=PromptManager(prompt_templates=prompts),
                azure_ai_connector=AIProvider(config)
            )
        raise ValueError(f"Unknown bot type: {bot_type}")