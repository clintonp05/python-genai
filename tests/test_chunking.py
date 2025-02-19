# tests/test_chunking.py
import unittest
from src.genai.core.processing.chunking.chunking import (
    FixedPositionChunker,
    RecursiveRetrieverChunker,
    ContextBasedChunker,
    ChunkingConfig
)

class TestChunkingStrategies(unittest.TestCase):
    def setUp(self):
        self.text = ("Section 1: Introduction\n\n"
                    "This is a sample document. It contains multiple sections. "
                    "Section 2: Content\n\nHere is the main content. "
                    "It has several paragraphs separated by newlines.")
        
    def test_fixed_chunking(self):
        config = ChunkingConfig(chunk_size=50, overlap=10)
        chunker = FixedPositionChunker(config)
        chunks = chunker.chunk(self.text)
        self.assertGreater(len(chunks), 3)
        self.assertTrue(all(len(chunk) <= 50 for chunk in chunks))

    def test_recursive_chunking(self):
        config = ChunkingConfig()
        chunker = RecursiveRetrieverChunker(config)
        chunks = chunker.chunk(self.text)
        self.assertGreater(len(chunks), 5)
        self.assertTrue(any('\n' in chunk for chunk in chunks))

    def test_context_chunking(self):
        config = ChunkingConfig()
        chunker = ContextBasedChunker(config)
        chunks = chunker.chunk(self.text)
        self.assertEqual(len(chunks), 2)
        self.assertTrue("Section 1" in chunks[0])
        self.assertTrue("Section 2" in chunks[1])

if __name__ == '__main__':
    unittest.main()