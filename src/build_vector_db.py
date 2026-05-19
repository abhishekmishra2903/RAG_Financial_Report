import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

HF_CACHE_DIR = BASE_DIR / "hf_cache"
HF_CACHE_DIR.mkdir(parents=True, exist_ok=True)

os.environ["HF_HOME"] = str(HF_CACHE_DIR)

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from schema_metadata import SCHEMA_METADATA
from config import VECTOR_DB_DIR, EMBEDDING_MODEL

documents = []

for table_info in SCHEMA_METADATA:

    text = f"""
    Table: {table_info['table']}

    Description:
    {table_info['description']}

    Columns:
    """

    for col, desc in table_info["columns"].items():
        text += f"\n- {col}: {desc}"

    documents.append(
        Document(
            page_content=text,
            metadata={"table": table_info["table"]}
        )
    )


embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector_db = FAISS.from_documents(
    documents,
    embedding_model
)

vector_db.save_local(str(VECTOR_DB_DIR))

print("Schema vector DB created successfully.")