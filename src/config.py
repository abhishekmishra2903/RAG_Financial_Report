from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "data" / "financial_report.db"

VECTOR_DB_DIR = BASE_DIR / "vector_store" / "faiss_index"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

LLM_MODEL = "tiiuae/falcon-7b-instruct"