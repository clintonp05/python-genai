from typing import List, Dict
from src.genai.config.settings import AzureAISearchConfig

class AzureSearchClient:
    def __init__(self, config: AzureAISearchConfig):
        self.endpoint = f"{config.endpoint}/indexes/{config.index_name}"
        self.headers = {
            "api-key": config.api_key,
            "Content-Type": "application/json"
        }
        self.config = config

    def upload_documents(self, documents: List[Dict]):
        url = f"{self.endpoint}/docs/index?api-version={self.config.api_version}"
        # Implementation using HTTPClient