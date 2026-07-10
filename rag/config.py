"""
Configuration settings for the RAG pipeline.
"""

# Embedding model
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

# Chunking
CHUNK_SIZE = 512
CHUNK_OVERLAP = 50

# Storage
STORAGE_DIR = "./storage"

# Number of retrieved chunks
TOP_K = 5