import os
from pathlib import Path
from datetime import datetime

# Hugging Face Cache + Mac M2 Stability Settings

BASE_DIR = Path(__file__).resolve().parent.parent

HF_CACHE_DIR = BASE_DIR / "hf_cache"
HF_CACHE_DIR.mkdir(parents=True, exist_ok=True)

os.environ["HF_HOME"] = str(HF_CACHE_DIR)

# Helps avoid MPS crashes on Mac
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"

# Output Directory

OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Imports

import torch
import pandas as pd
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    pipeline
)

from sql_executor import execute_sql
from sql_templates import SQL_TEMPLATES

# Falcon 7B Model Setup

MODEL_NAME = "tiiuae/falcon-7b-instruct"

print("Loading Falcon tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

print("Loading Falcon 7B model...")
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16,
    device_map="auto",
    low_cpu_mem_usage=True
)

print("Creating generation pipeline...")
generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=450,       
    do_sample=False,          # Max factual determination
    repetition_penalty=1.1    
)

# Safe column whitelist to protect Falcon's context window (2048 token limit)
ESSENTIAL_COLUMNS = {
    "computed_metrics_summary": ["metric", "value"],
    "income_statement_summary": ["date", "revenue", "netIncome", "operatingIncome", "ebitda", "eps"],
    "balance_sheet_summary": ["date", "totalAssets", "totalLiabilities", "totalDebt", "cashAndCashEquivalents", "totalStockholdersEquity"],
    "cashflow_summary": ["date", "operatingCashFlow", "freeCashFlow", "capitalExpenditure"],
    "economic_summary": ["date", "indicator", "value", "indicators"]
}

# Financial Report Generator

def generate_financial_report(question: str):

    print("Executing comprehensive SQL data extraction...")
    
    result_texts = []
    for section_name, sql_query in SQL_TEMPLATES.items():
        try:
            query_result = execute_sql(sql_query)
            if query_result is None or query_result.empty:
                 result_texts.append(f"=== {section_name.upper()} DATA ===\nData is empty.")
            else:
                 # Clean up empty data
                 query_result = query_result.dropna(axis=1, how='all')
                 
                 # SAFE PYTHON FILTER: Keep only crucial columns if they exist in the DB
                 whitelist = ESSENTIAL_COLUMNS.get(section_name, query_result.columns)
                 valid_cols = [col for col in whitelist if col in query_result.columns]
                 query_result = query_result[valid_cols]
                 
                 # Flatten into clean, compact key-value lines
                 formatted_rows = []
                 for _, row in query_result.iterrows():
                     row_str = " | ".join([f"{col}: {val}" for col, val in row.items() if pd.notna(val)])
                     formatted_rows.append(f"- {row_str}")
                 
                 section_data = "\n".join(formatted_rows)
                 result_texts.append(f"=== {section_name.upper()} DATA ===\n{section_data}")
        except Exception as e:
            print(f"❌ SQL Error in '{section_name}': {e}")
            result_texts.append(f"=== {section_name.upper()} DATA ===\nData not available.")

    combined_sql_results = "\n\n".join(result_texts)

    # Final Factual Prompt
    prompt = f"""You are a strict, factual financial data analyst.
Your ONLY job is to write a report using the EXACT numbers provided in the "SQL DATA" section below.

CRITICAL INSTRUCTIONS:
- DO NOT invent, assume, extrapolate, or calculate any numbers. If a number is not explicitly present in the SQL DATA, do not mention it.
- State specific numerical values and dates from the data for EVERY observation you make. Do not write generic summaries without including the numbers.
- Keep your sentences concise, objective, and strictly professional.

QUESTION:
{question}

SQL DATA (USE ONLY THIS DATA FOR YOUR NUMBERS):
{combined_sql_results}

Write a concise report with exactly these sections:
1. Profitability & Growth
2. Debt Condition
3. Cash Flow
4. Economic Outlook
5. Final Assessment

REPORT:
"""

    print("\nGenerating final report using Falcon 7B...\n")

    response = generator(
        prompt,
        truncation=True,
        pad_token_id=tokenizer.eos_token_id
    )

    generated_text = response[0]["generated_text"]
    final_answer = generated_text[len(prompt):].strip()

    return final_answer

# Save Report as Markdown

def save_report_markdown(report_text: str):

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"financial_report_{timestamp}.md"
    report_path = OUTPUT_DIR / report_filename

    markdown_content = f"""# Financial Report

Generated On: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

{report_text}
"""

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)

    print(f"\nReport saved successfully:\n{report_path}")

# Main

if __name__ == "__main__":

    question = """
    Generate a comprehensive financial summary of the company,
    including profitability, debt condition, cash flow strength,
    growth trends and macroeconomic outlook.
    """

    answer = generate_financial_report(question)

    print("\n================ FINAL REPORT ================\n")
    print(answer)

    save_report_markdown(answer)