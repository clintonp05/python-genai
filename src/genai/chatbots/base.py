from pydantic import BaseModel
from abc import ABC, abstractmethod

class ChatRequest(BaseModel):
    message: str
    context: dict = {}

class ChatResponse(BaseModel):
    message: str
    metadata: dict = {}

class Chatbot(ABC):
    @abstractmethod
    def chat(self, request: ChatRequest) -> ChatResponse:
        pass