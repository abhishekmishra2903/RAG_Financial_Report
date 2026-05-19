import os
from pathlib import Path

import requests
import pandas as pd
from dotenv import load_dotenv

# Project paths

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR /  "data" / "raw"
DATA_DIR = BASE_DIR / "data"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Load environment variables

load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("FMP_API_KEY")

if not API_KEY:
    raise ValueError(
        "FMP_API_KEY not found. Please check your .env file in the project root."
    )

# Configuration

STABLE_URL = "https://financialmodelingprep.com/stable"

symbol = "MSFT"
limit = 5

# Utility functions

def hide_api_key(text: str) -> str:
    """
    Hide API key before printing URLs or error messages.
    """
    if not text:
        return text
    return text.replace(API_KEY, "API_KEY_HIDDEN")


def fetch_fmp(endpoint: str, params: dict | None = None):
    """
    Generic Financial Modeling Prep stable endpoint fetcher.
    """
    if params is None:
        params = {}

    params = params.copy()
    params["apikey"] = API_KEY

    url = f"{STABLE_URL}/{endpoint}"

    try:
        response = requests.get(url, params=params, timeout=30)

        print("\n----------------------------------------")
        print(f"Endpoint: {endpoint}")
        print("Request URL:", hide_api_key(response.url))
        print("Status code:", response.status_code)

        if response.status_code != 200:
            print("Error response:", hide_api_key(response.text[:1000]))
            return []

        data = response.json()

        if isinstance(data, dict) and "Error Message" in data:
            print("FMP error:", data)
            return []

        if data is None:
            print("No data returned.")
            return []

        return data

    except requests.exceptions.RequestException as e:
        print(f"Request failed for endpoint '{endpoint}':", e)
        return []

    except Exception as e:
        print(f"Unexpected error for endpoint '{endpoint}':", e)
        return []


def to_dataframe(data, dataset_name: str) -> pd.DataFrame:
    """
    Convert API response to DataFrame safely.
    """
    if isinstance(data, list):
        df = pd.DataFrame(data)
    elif isinstance(data, dict):
        df = pd.DataFrame([data])
    else:
        df = pd.DataFrame()

    print(f"{dataset_name} shape:", df.shape)
    return df


def save_csv(df: pd.DataFrame, filename: str):
    """
    Save DataFrame to outputs folder.
    """
    path = OUTPUT_DIR / filename
    df.to_csv(path, index=False)
    print(f"Saved: {path}")

# Fetch functions

def fetch_company_profile(symbol: str):
    return fetch_fmp(
        endpoint="profile",
        params={"symbol": symbol}
    )


def fetch_stock_quote(symbol: str):
    return fetch_fmp(
        endpoint="quote",
        params={"symbol": symbol}
    )


def fetch_income_statement(symbol: str, limit: int = 5):
    return fetch_fmp(
        endpoint="income-statement",
        params={
            "symbol": symbol,
            "limit": limit
        }
    )


def fetch_balance_sheet(symbol: str, limit: int = 5):
    return fetch_fmp(
        endpoint="balance-sheet-statement",
        params={
            "symbol": symbol,
            "limit": limit
        }
    )


def fetch_cash_flow(symbol: str, limit: int = 5):
    return fetch_fmp(
        endpoint="cash-flow-statement",
        params={
            "symbol": symbol,
            "limit": limit
        }
    )


def fetch_economic_indicator(indicator_name: str):
    return fetch_fmp(
        endpoint="economic-indicators",
        params={"name": indicator_name}
    )


# Main execution

print(f"Fetching financial data for symbol: {symbol}")

# Company profile
profile_data = fetch_company_profile(symbol)
profile_df = to_dataframe(profile_data, "company_profile")
save_csv(profile_df, "company_profile.csv")

# Stock quote
quote_data = fetch_stock_quote(symbol)
quote_df = to_dataframe(quote_data, "stock_quote")
save_csv(quote_df, "stock_quote.csv")

# Income statement
income_data = fetch_income_statement(symbol, limit=limit)
income_df = to_dataframe(income_data, "income_statement")
save_csv(income_df, "income_statement.csv")

# Balance sheet
balance_data = fetch_balance_sheet(symbol, limit=limit)
balance_df = to_dataframe(balance_data, "balance_sheet")
save_csv(balance_df, "balance_sheet.csv")

# Cash flow statement
cashflow_data = fetch_cash_flow(symbol, limit=limit)
cashflow_df = to_dataframe(cashflow_data, "cash_flow")
save_csv(cashflow_df, "cash_flow.csv")

# Economic indicators

indicators = [
    "GDP",
    "unemploymentRate",
    "inflationRate"
]

economic_frames = []

for indicator in indicators:
    print(f"\nFetching economic indicator: {indicator}")

    data = fetch_economic_indicator(indicator)
    df = to_dataframe(data, f"economic_indicator_{indicator}")

    if not df.empty:
        df["indicator"] = indicator
        economic_frames.append(df)
    else:
        print(f"No data found for indicator: {indicator}")

if economic_frames:
    economic_df = pd.concat(economic_frames, ignore_index=True)
else:
    economic_df = pd.DataFrame()

save_csv(economic_df, "economic_indicators.csv")

# Preview

print("\n========================================")
print("Fetch completed.")
print("========================================")

print("\nCompany Profile Preview:")
print(profile_df.head())

print("\nStock Quote Preview:")
print(quote_df.head())

print("\nIncome Statement Preview:")
print(income_df.head())

print("\nBalance Sheet Preview:")
print(balance_df.head())

print("\nCash Flow Preview:")
print(cashflow_df.head())

print("\nEconomic Indicators Preview:")
print(economic_df.head())