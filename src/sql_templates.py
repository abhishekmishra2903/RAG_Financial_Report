SQL_TEMPLATES = {
    "computed_metrics_summary":
    """
    SELECT *
    FROM computed_metrics
    """,

    "income_statement_summary":
    """
    SELECT *
    FROM income_statement
    ORDER BY date DESC
    LIMIT 3
    """,

    "balance_sheet_summary":
    """
    SELECT *
    FROM balance_sheet
    ORDER BY date DESC
    LIMIT 1
    """,

    "cashflow_summary":
    """
    SELECT *
    FROM cash_flow
    ORDER BY date DESC
    LIMIT 1
    """,

    "economic_summary":
    """
    SELECT *
    FROM economic_indicators
    ORDER BY date DESC
    LIMIT 5
    """
}