from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from .config import EMBEDDING_MODEL

# Configure the embedding model globally so every index build/load
# (build_index, get_or_create_index, get_retriever) uses the same one.
Settings.embed_model = HuggingFaceEmbedding(model_name=EMBEDDING_MODEL)

from .loader import load_documents
from .indexer import build_index
from .storage_manager import get_or_create_index
from .retriever import get_retriever