from pathlib import Path
from typing import List
from  src.genai.core.processing.chunking.chunking import ChunkingStrategy, FixedPositionChunker

class DocumentProcessor:
    """Process documents using configured chunking strategy"""
    
    def __init__(self, chunker: ChunkingStrategy = None):
        self.chunker = chunker or FixedPositionChunker()

    def process_file(self, file_path: Path) -> List[str]:
        with open(file_path, 'r') as f:
            content = f.read()
        return self.chunker.chunk(content)

    def process_batch(self, files: List[Path]) -> List[List[str]]:
        return [self.process_file(f) for f in files]