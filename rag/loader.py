from pathlib import Path

from llama_index.core import SimpleDirectoryReader


def load_documents(data_dir="data/uploads"):
    """
    Load all documents from the uploads folder.
    """

    reader = SimpleDirectoryReader(
        input_dir=data_dir
    )

    documents = reader.load_data()

    print(f"Loaded {len(documents)} document(s).")

    return documents