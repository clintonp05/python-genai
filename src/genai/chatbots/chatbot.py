# base.py
from abc import ABC, abstractmethod
from pydantic import BaseModel

from src.genai.config.prompts import PromptManager

class ChatRequest(BaseModel):
    message: str
    context: dict = {}

class Chatbot(ABC):
    @abstractmethod
    def chat(self, request: ChatRequest) -> str:
        pass

# standard.py
class StandardBot(Chatbot):
    def chat(self, request: ChatRequest) -> str:
        return f"Response to: {request.message}"

# rag.py
from ..rag import Retriever

class RAGBot(Chatbot):
    def __init__(self, retriever: Retriever, prompt_manager: PromptManager):
        self.retriever = retriever
        self.prompts = prompt_manager

    def chat(self, request: ChatRequest) -> str:
        context = self.retriever.search(request.message)
        template = self.prompts.get_template("default")
        return template.template.format(
            query=request.message,
            context=context
        )