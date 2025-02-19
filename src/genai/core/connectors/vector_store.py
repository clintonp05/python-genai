from typing import List, Dict
from src.genai.core.connectors.http_connector import HTTPClient
from src.genai.utils.di import DIContainer
from src.genai.config.settings import AppConfig

class VectorStore:
    def __init__(self, config: AppConfig):
        self.config = config
        self.http = DIContainer.resolve(HTTPClient)

    def batch_upload(self, embeddings: List[Dict]):
        for batch in self._chunk_data(embeddings):
            self.http.post(
                f"{self.config.ai_search.endpoint}/batch",
                json={"documents": batch}
            )

    def _chunk_data(self, data: List, size: int = 1000):
        for i in range(0, len(data), size):
            yield data[i:i+size]

    def search(self, query: str, top_k: int = 15):
        return {
            "results": [
                {"id": 1, "text": "This is a test", "score": 0.9}
            ]
        }