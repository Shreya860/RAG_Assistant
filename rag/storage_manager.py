from pathlib import Path

from llama_index.core import StorageContext, load_index_from_storage

from rag.config import STORAGE_DIR
from rag.indexer import build_index


def get_or_create_index(documents):
    """
    Load an existing index if available,
    otherwise build and save a new one.
    """

    storage_path = Path(STORAGE_DIR)

    if storage_path.exists() and any(storage_path.iterdir()):
        print("Loading existing index...")

        storage_context = StorageContext.from_defaults(
            persist_dir=STORAGE_DIR
        )

        index = load_index_from_storage(storage_context)

    else:
        print("No existing index found.")
        print("Building a new index...")

        index = build_index(documents)

    return index