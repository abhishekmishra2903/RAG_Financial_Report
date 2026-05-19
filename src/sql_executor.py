import sqlite3
import pandas as pd

from config import DB_PATH


def execute_sql(query: str):

    conn = sqlite3.connect(DB_PATH)

    try:
        df = pd.read_sql_query(query, conn)
        return df

    finally:
        conn.close()