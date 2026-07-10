from llama_index.core import VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from rag.config import (
    EMBEDDING_MODEL,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    STORAGE_DIR,
)


def build_index(documents):
    """
    Build a vector index from the loaded documents
    and save it locally.
    """

    # Load embedding model
    embed_model = HuggingFaceEmbedding(
        model_name=EMBEDDING_MODEL
    )

    # Create a text splitter
    splitter = SentenceSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    # Split documents into nodes (chunks)
    nodes = splitter.get_nodes_from_documents(documents)

    # Build vector index
    index = VectorStoreIndex(
        nodes,
        embed_model=embed_model,
    )

    # Save the index locally
    index.storage_context.persist(
        persist_dir=STORAGE_DIR
    )

    print(f"Indexed {len(nodes)} chunks.")

    return index