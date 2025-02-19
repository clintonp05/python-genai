from pydantic import BaseModel
from typing import List, Dict
from src.genai.core.connectors.vector_store import VectorStore

class RetrievalRequest(BaseModel):
    query: str
    top_k: int = 5

class Retriever:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store

    def search(self, request: RetrievalRequest) -> List[Dict]:
        return self.vector_store.search(
            query=request.query,
            top_k=request.top_k
        )