from llama_index.core import StorageContext, load_index_from_storage

from rag.config import STORAGE_DIR, TOP_K


def get_retriever():
    """
    Load the saved vector index and return a retriever.
    """

    storage_context = StorageContext.from_defaults(
        persist_dir=STORAGE_DIR
    )

    index = load_index_from_storage(
        storage_context
    )

    retriever = index.as_retriever(
        similarity_top_k=TOP_K
    )

    return retriever