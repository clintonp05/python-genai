from typing import List
import numpy as np
from pydantic import BaseModel
from src.genai.core.connectors.http_connector import HTTPClient
from src.genai.utils.di import DIContainer
from src.genai.config.settings import AppConfig, AzureOpenAIConfig

class EmbeddingRequest(BaseModel):
    texts: List[str]
    model: str = "text-embedding-ada-002"

class AIProvider:
    def __init__(self, config: AppConfig):
        self.endpoint = f"{config.openai.endpoint}/openai/deployments/{config.openai.model}"
        self.headers = {
            "Content-Type": "application/json"
        }
        self.params = {
            "api-key": config.openai.api_key,
            "api-version": config.openai.api_version
        }
        self.config = config

    def get_embeddings(self, texts: List[str]):
        url = f"{self.endpoint}/embeddings"
        # Implementation using HTTPClient
        # Send the request to the Azure OpenAI service
        response = HTTPClient(config=self.config).execute_request(
            method='POST',
            url=url,
            headers=self.headers,
            body={"input" : texts},
            params=self.params
        )
        
        # Check if the response is successful
        if response.status_code == 200:
            response_data = response.json()
            embeddings = response_data.get("data", [])
            return np.array([embedding["embedding"] for embedding in embeddings])
        else:
            response.raise_for_status()

    def generate_response(self, messages: list[str]):
        url = f"{self.endpoint}/chat/completions?api-version={self.config.openai.api_version}&api-key={self.config.openai.api_key}"
        payload = {
            "messages": messages,
            "max_tokens": 150,
            "temperature": 0.7,
            "top_p": 1,
            "n": 1
        }
        
        # Send the request to the Azure OpenAI service
        response = HTTPClient(config=self.config).execute_request(method='POST',url=url, headers=self.headers, payload=payload, params=self.params)
        
        # Check if the response is successful
        if response.status_code == 200:
            response_data = response.json()
            print("response_data ",response_data)
            return response_data.get("choices", [{}])[0].get("text", "").strip()
        else:
            response.raise_for_status()