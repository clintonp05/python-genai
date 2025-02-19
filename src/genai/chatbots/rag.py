from pydantic import BaseModel
from src.genai.chatbots.base import ChatRequest, Chatbot
from src.genai.config.prompts import PromptManager, PromptTemplate
from src.genai.core.connectors.ai_provider import AIProvider
from src.genai.rag.retriever import RetrievalRequest, Retriever
from ..config.settings import AppConfig, ChatbotConfig, AzureOpenAIConfig

class AzureOpenAIMessage(BaseModel):
    role: str
    content: str

class RAGBot(Chatbot):
    def __init__(self, config: AppConfig, retriever : Retriever ,prompt_manager: PromptManager, azure_ai_connector:AIProvider):
        self.config = config
        self.prompts = prompt_manager
        self.retriever = retriever
        self.ai_provider = azure_ai_connector

    def chat(self, request: ChatRequest) -> str:
        context = self.retriever.search(RetrievalRequest(query=request.message, top_k=5))
        template = self.prompts.get_template("default")
        print('template',self.prompts)
        # Send the formatted prompt to Azure OpenAI and get the response
        response = self.ai_provider.generate_response(messages=self.prepare_message(request, template, context=context))
        return response

    def prepare_message(self, request: ChatRequest, prompt_template: PromptTemplate, context: str) -> list[AzureOpenAIMessage]:
        return [
            AzureOpenAIMessage(role="user", content=request.message),
            AzureOpenAIMessage(role="system", content=prompt_template.template.format(query=request.message, context=context))
        ]
