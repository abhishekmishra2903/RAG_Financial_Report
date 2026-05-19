# Financial Report Generation using RAG and Economic Indicators

## Project Overview

This project builds a Retrieval-Augmented Generation (RAG) based financial reporting system using the latest financial and macroeconomic data of Microsoft Corporation (MSFT) fetched from the Financial Modeling Prep (FMP) API.

The system generates concise financial summaries without training or fine-tuning any LLM or ML model. Instead, it combines structured SQL-based retrieval with semantic schema retrieval and uses the Falcon 7B Instruct open-source LLM for final report generation.

The project demonstrates how structured financial datasets can be integrated with modern RAG pipelines while maintaining factual consistency in generated financial reports.

---

## Problem Statement

Build a short financial report generation system using:
- Microsoft Corporation (MSFT) financial statements
- Stock market metrics
- Economic indicators

Constraints:
- No model training
- No fine-tuning
- Use open-source APIs and open-source LLMs

---

## Features

- Fetches latest Microsoft Corporation (MSFT) financial data using Financial Modeling Prep API
- Retrieves macroeconomic indicators such as:
  - GDP
  - Inflation Rate
  - Unemployment Rate
- Preprocesses and cleans financial datasets
- Stores processed data in:
  - CSV files
  - SQLite database
- Builds a schema-aware Vector Database using FAISS
- Uses Hugging Face embeddings for semantic retrieval
- Implements RAG architecture using LangChain
- Uses Falcon 7B Instruct for report generation
- Generates concise factual financial summaries

---

## Workflow

### 1. Data Collection

Financial and economic data related to Microsoft Corporation (MSFT) are fetched from FMP API:
- Company Profile
- Stock Quote
- Income Statement
- Balance Sheet
- Cash Flow Statement
- Economic Indicators

Implemented in:
- `fetch_data.py` :contentReference[oaicite:0]{index=0}

---

## Sample Generated Report

```text
The company performed strongly in FY2025, with revenue growth of 14.93% and net income growth of 15.54% compared to FY2024. The debt-to-equity ratio stood at 0.8 in FY2025, indicating moderate financial leverage. Free cash flow reached $71.61 billion, while capital expenditure was -$64.55 billion in FY2025. The inflation rate was 2.49% in May 2026, slightly above the 2.25% target range. Overall, macroeconomic indicators suggest a stable and potentially growing market environment.
```

---

## Conclusion

This project demonstrates a practical financial RAG architecture using Microsoft Corporation (MSFT) financial data by combining:
- structured SQL retrieval
- semantic schema retrieval
- open-source embeddings
- Falcon 7B LLM

while avoiding hallucinated financial values and maintaining factual consistency.
