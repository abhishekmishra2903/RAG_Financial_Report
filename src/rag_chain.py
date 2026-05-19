import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

HF_CACHE_DIR = BASE_DIR / "hf_cache"

HF_CACHE_DIR.mkdir(parents=True, exist_ok=True)

os.environ["HF_HOME"] = str(HF_CACHE_DIR)
from transformers import pipeline
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from config import VECTOR_DB_DIR, EMBEDDING_MODEL
from sql_templates import SQL_TEMPLATES


embedding_model = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL
)

vector_db = FAISS.load_local(
    str(VECTOR_DB_DIR),
    embedding_model,
    allow_dangerous_deserialization=True
)

retriever = vector_db.as_retriever(search_kwargs={"k": 2})


def retrieve_schema_context(question: str):

    docs = retriever.invoke(question)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    return context
def retrieve_financial_context(query: str, k: int = 5):

    docs = vector_db.similarity_search(query, k=k)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    return context


def retrieve_economic_context(query: str, k: int = 3):

    economic_query = f"""
    economic indicators macroeconomic outlook GDP inflation interest rates
    {query}
    """

    docs = vector_db.similarity_search(economic_query, k=k)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    return context
