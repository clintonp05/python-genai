from typing import List
import numpy as np
from src.genai.core.connectors.ai_provider import AIProvider

class BatchEmbedder:
    def __init__(self, ai_provider: AIProvider, batch_size: int = 512):
        self.provider = ai_provider
        self.batch_size = batch_size

    def generate_embeddings(self, texts: List[str]) -> List[np.ndarray]:
        return [
            self.provider.get_embeddings(batch)
            for batch in self._batch_generator(texts)
        ]

    def _batch_generator(self, texts: List[str]):
        for i in range(0, len(texts), self.batch_size):
            yield texts[i:i+self.batch_size]