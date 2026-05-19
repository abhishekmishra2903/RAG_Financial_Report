SCHEMA_METADATA = [

    {
        "table": "company_profile",
        "description": "Contains company basic profile information.",
        "columns": {
            "companyName": "Company name",
            "sector": "Business sector",
            "industry": "Business industry",
            "marketCap": "Total market capitalization",
            "price": "Current stock price",
            "beta": "Volatility indicator",
            "ceo": "Chief executive officer"
        }
    },

    {
        "table": "income_statement",
        "description": "Contains company revenue and profitability metrics.",
        "columns": {
            "revenue": "Total company revenue",
            "grossProfit": "Gross profit",
            "operatingIncome": "Operating income",
            "netIncome": "Net income after tax",
            "eps": "Earnings per share",
            "ebitda": "EBITDA"
        }
    },

    {
        "table": "balance_sheet",
        "description": "Contains company assets, liabilities and equity.",
        "columns": {
            "totalAssets": "Total assets",
            "totalLiabilities": "Total liabilities",
            "totalDebt": "Total debt",
            "cashAndCashEquivalents": "Cash reserves",
            "totalStockholdersEquity": "Shareholder equity"
        }
    },

    {
        "table": "cash_flow",
        "description": "Contains company cash flow metrics.",
        "columns": {
            "operatingCashFlow": "Cash from operations",
            "freeCashFlow": "Free cash flow",
            "capitalExpenditure": "Capital expenditure"
        }
    },

    {
        "table": "economic_indicators",
        "description": "Contains macroeconomic indicators.",
        "columns": {
            "indicator": "Economic indicator name",
            "value": "Indicator value",
            "date": "Indicator date"
        }
    },

    {
        "table": "computed_metrics",
        "description": "Contains precomputed financial metrics.",
        "columns": {
            "metric": "Metric name",
            "value": "Metric value"
        }
    }
]