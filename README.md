# Financial Report Generation using RAG and Economic Indicators

## Project Overview

This project builds a Retrieval-Augmented Generation (RAG) based financial reporting system using the latest financial and macroeconomic data of Microsoft Corporation (MSFT) fetched from the Financial Modeling Prep (FMP) API.

The system generates concise financial summaries without training or fine-tuning any LLM or ML model. Instead, it combines structured SQL-based retrieval with semantic schema retrieval and uses the Falcon 7B Instruct open-source LLM for final report generation.

The project demonstrates how structured financial datasets can be integrated with modern RAG pipelines while maintaining factual consistency in generated financial reports.

---

## Problem Statement

Build a short financial report generation system using:
- Company financial statements
- Stock market metrics
- Economic indicators

Constraints:
- No model training
- No fine-tuning
- Use open-source APIs and open-source LLMs

---

## Features

- Fetches latest company financial data using Financial Modeling Prep API
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

## Architecture

User Query
↓
Schema Retrieval using Vector DB
↓
SQL Template Selection
↓
SQLite Query Execution
↓
Structured Financial Data
↓
Falcon 7B Report Generation

---

## Project Structure

```text
RAG_FINANCIAL_REPORT/

├── data/
│   ├── raw/
│   ├── processed/
│   └── financial_report.db
│
├── outputs/
│
├── src/
│   ├── fetch_data.py
│   ├── preprocess.py
│   ├── build_vector_db.py
│   ├── schema_metadata.py
│   ├── sql_templates.py
│   ├── sql_executor.py
│   ├── rag_chain.py
│   ├── report_generator.py
│   └── config.py
│
├── vector_store/
├── hf_cache/
├── requirements.txt
└── README.md
```

---

## Workflow

### 1. Data Collection

Financial and economic data are fetched from FMP API:
- Company Profile
- Stock Quote
- Income Statement
- Balance Sheet
- Cash Flow Statement
- Economic Indicators

Implemented in:
- `fetch_data.py` :contentReference[oaicite:0]{index=0}

---

### 2. Data Preprocessing

The fetched datasets are:
- cleaned
- validated
- converted to proper numeric types
- transformed into structured tables

Additional computed metrics include:
- revenue growth
- net income growth
- debt-to-equity ratio
- net debt
- free cash flow

Processed data is stored in:
- CSV files
- SQLite database

Implemented in:
- `preprocess.py` :contentReference[oaicite:1]{index=1}

---

### 3. Schema-Aware Vector Database

Instead of embedding raw numerical financial rows, only:
- table descriptions
- column meanings
- schema metadata

are embedded using:
- Hugging Face embeddings
- FAISS vector database

This improves factual reliability.

Implemented in:
- `build_vector_db.py` :contentReference[oaicite:2]{index=2}
- `schema_metadata.py` :contentReference[oaicite:3]{index=3}

---

### 4. SQL-Based Retrieval

The system uses predefined SQL templates to retrieve exact financial values from SQLite.

Implemented in:
- `sql_templates.py` :contentReference[oaicite:4]{index=4}
- `sql_executor.py` :contentReference[oaicite:5]{index=5}

---

### 5. RAG Pipeline

LangChain retrieves relevant schema context from the FAISS vector store.

Implemented in:
- `rag_chain.py` :contentReference[oaicite:6]{index=6}

---

### 6. Report Generation using Falcon 7B

The retrieved SQL results are provided to Falcon 7B Instruct to generate a concise financial report.

Implemented in:
- `report_generator.py` :contentReference[oaicite:7]{index=7}

---

## Technologies Used

- Python
- LangChain
- FAISS
- SQLite
- Hugging Face Transformers
- Falcon 7B Instruct
- Sentence Transformers
- Pandas
- Financial Modeling Prep API

---

## Sample Generated Report

```text
The company performed strongly in FY2025, with revenue growth of 14.93% and net income growth of 15.54% compared to FY2024. The debt-to-equity ratio stood at 0.8 in FY2025, indicating moderate financial leverage. Free cash flow reached $71.61 billion, while capital expenditure was -$64.55 billion in FY2025. The inflation rate was 2.49% in May 2026, slightly above the 2.25% target range. Overall, macroeconomic indicators suggest a stable and potentially growing market environment.
```

---

## Important Design Decisions

### Why raw financial rows were not embedded

Embedding raw numerical financial records can produce:
- incorrect value retrieval
- hallucinated financial metrics
- unreliable numerical similarity matches

Instead:
- schema metadata was embedded
- SQL was used for exact numerical retrieval

This improves factual consistency significantly.

---

## Limitations

- Falcon 7B has a 2048 token context limit
- Long prompts may slow down inference on local systems
- SQL outputs were intentionally restricted using `LIMIT` clauses to remain within the model context window

---

## Future Improvements

- Dynamic SQL generation
- Multi-agent financial analysis
- Real-time dashboard integration
- Financial trend visualization
- SEC filing integration
- PDF report generation
- Cloud deployment

---

## How to Run

### Install dependencies

```bash
pip install -r requirements.txt
```

### Step 1: Fetch Data

```bash
python src/fetch_data.py
```

### Step 2: Preprocess Data

```bash
python src/preprocess.py
```

### Step 3: Build Vector DB

```bash
python src/build_vector_db.py
```

### Step 4: Generate Report

```bash
python src/report_generator.py
```

---

## Conclusion

This project demonstrates a practical financial RAG architecture combining:
- structured SQL retrieval
- semantic schema retrieval
- open-source embeddings
- Falcon 7B LLM

while avoiding hallucinated financial values and maintaining factual consistency.
