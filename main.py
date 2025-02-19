from functools import lru_cache
import os
from dotenv import load_dotenv

from src.genai.chatbots.chatbot import ChatRequest
from src.genai.chatbots import ChatbotFactory
from src.genai.config.settings import AppConfig 

print("Hello AI Engineer!")

# Load environment variables from .env file
load_dotenv(dotenv_path='/Users/clinton/POC/projects/leap-python-genai/.env')

@lru_cache
def get_settings():
    return AppConfig()

config = get_settings()

print(f"AZURE_OPENAI_ENDPOINT: {config.ai_search.endpoint}")
print(f"AZURE_OPENAI_API_KEY: {os.getenv('AZURE_OPENAI_API_KEY')}")
print(f"AZURE_OPENAI_API_VERSION: {os.getenv('AZURE_OPENAI_API_VERSION')}")
print(f"AZURE_OPENAI_MODEL: {os.getenv('AZURE_OPENAI_MODEL')}")

print(f"Using AI model: {config.openai.api_key}")
print(f"Vector store URL: {config.ai_search.endpoint}")

bot = ChatbotFactory.create("rag", config)
response = bot.chat(ChatRequest(message="Hello AI!"))