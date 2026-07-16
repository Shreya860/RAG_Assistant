from llama_index.core import VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter

from rag.config import (
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    STORAGE_DIR,
)


def build_index(documents):
    """
    Build a vector index from the loaded documents
    and save it locally.
    """

    # Create a text splitter
    splitter = SentenceSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    # Split documents into nodes (chunks)
    nodes = splitter.get_nodes_from_documents(documents)

    # Build vector index (uses Settings.embed_model, configured in rag/__init__.py)
    index = VectorStoreIndex(nodes)

    # Save the index locally
    index.storage_context.persist(
        persist_dir=STORAGE_DIR
    )

    print(f"Indexed {len(nodes)} chunks.")

    return index