# base.py
from abc import ABC, abstractmethod
from pydantic import BaseModel

class ChunkingConfig(BaseModel):
    chunk_size: int = 512
    overlap: int = 50

class ChunkingStrategy(ABC):
    def __init__(self, config: ChunkingConfig):
        self.config = config
        
    @abstractmethod
    def chunk(self, text: str) -> list[str]:
        pass

# fixed.py
class FixedPositionChunker(ChunkingStrategy):
    def chunk(self, text: str) -> list[str]:
        return [text[i:i+self.config.chunk_size] 
               for i in range(0, len(text), self.config.chunk_size - self.config.overlap)]

# recursive.py
class RecursiveRetrieverChunker(ChunkingStrategy):
    def chunk(self, text: str) -> list[str]:
        separators = ["\n\n", ". ", "! ", "? ", "; "]
        chunks = [text]
        for sep in separators:
            chunks = [sub_chunk for chunk in chunks 
                     for sub_chunk in chunk.split(sep)]
        return chunks

# context.py
class ContextBasedChunker(ChunkingStrategy):
    def chunk(self, text: str) -> list[str]:
        return re.split(r"(?:Section|Chapter|Topic) \d+", text)