from pathlib import Path
from typing import List, Any, Type
from langchain_community.document_loaders import (
    PyPDFLoader, TextLoader, CSVLoader, 
    UnstructuredExcelLoader, Docx2txtLoader, JSONLoader
)

def load_all_documents(data_dir: str) -> List[Any]:
    """
    Load supported files using a mapping strategy to reduce redundancy.
    """
    data_path = Path(data_dir).resolve()
    documents = []

    # Map file extensions to their respective LangChain loader classes
    LOADER_MAPPING: dict[str, Type] = {
        ".pdf": PyPDFLoader,
        ".txt": TextLoader,
        ".csv": CSVLoader,
        ".xlsx": UnstructuredExcelLoader,
        ".docx": Docx2txtLoader,
        ".json": JSONLoader,
    }

    print(f"[DEBUG] Scanning directory: {data_path}")

    # Iterate through all files in the directory recursively
    for file_path in data_path.rglob("*"):
        if file_path.suffix in LOADER_MAPPING:
            loader_class = LOADER_MAPPING[file_path.suffix]
            print(f"[DEBUG] Loading {file_path.suffix.upper()}: {file_path.name}")
            
            try:
                # Initialize loader (Note: JSONLoader might need jq_schema)
                loader = loader_class(str(file_path))
                documents.extend(loader.load())
            except Exception as e:
                print(f"[ERROR] Failed to load {file_path.name}: {e}")

    print(f"[DEBUG] Total documents loaded: {len(documents)}")
    return documents