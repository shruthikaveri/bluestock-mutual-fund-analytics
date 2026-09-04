import sqlite3
import pandas as pd
from pathlib import Path

# ==========================================
# BLUESTOCK DAY 2 - SQL QUERY TESTING
# ==========================================

DATABASE_FILE = "bluestock_mf.db"

REPORT_FOLDER = Path("reports")
REPORT_FOLDER.mkdir(exist_ok=True)

OUTPUT_FILE = REPORT_FOLDER / "sql_query_results.txt"


# ==========================================
# CONNECT TO DATABASE
# ==========================================

conn = sqlite3.connect(DATABASE_FILE)

print("\n===== RUNNING 10 SQL ANALYTICAL QUERIES =====\n")


# ==========================================
# SQL QUERIES
# ==========================================

queries = {

    "QUERY 1 - TOP 10 FUNDS BY 3-YEAR RETURN": """
        SELECT
            scheme_name,
            fund_house,
            category,
            return_3yr_pct
        FROM fact_performance
        ORDER BY return_3yr_pct DESC
        LIMIT 10;
    """,

    "QUERY 2 - TOP 10 FUNDS BY 5-YEAR RETURN": """
        SELECT
            scheme_name,
            fund_house,
            category,
            return_5yr_pct
        FROM fact_performance
        ORDER BY return_5yr_pct DESC
        LIMIT 10;
    """,

    "QUERY 3 - AVERAGE 3-YEAR RETURN BY FUND HOUSE": """
        SELECT
            fund_house,
            ROUND(AVG(return_3yr_pct), 2) AS average_3yr_return
        FROM fact_performance
        GROUP BY fund_house
        ORDER BY average_3yr_return DESC;
    """,

    "QUERY 4 - CATEGORY-WISE PERFORMANCE": """
        SELECT
            category,
            ROUND(AVG(return_1yr_pct), 2) AS average_1yr_return,
            ROUND(AVG(return_3yr_pct), 2) AS average_3yr_return,
            ROUND(AVG(return_5yr_pct), 2) AS average_5yr_return
        FROM fact_performance
        GROUP BY category
        ORDER BY average_3yr_return DESC;
    """,

    "QUERY 5 - TOP 10 FUNDS BY SHARPE RATIO": """
        SELECT
            scheme_name,
            fund_house,
            return_3yr_pct,
            sharpe_ratio,
            risk_grade
        FROM fact_performance
        ORDER BY sharpe_ratio DESC
        LIMIT 10;
    """,

    "QUERY 6 - TRANSACTION AMOUNT BY TYPE": """
        SELECT
            transaction_type,
            COUNT(*) AS total_transactions,
            SUM(amount_inr) AS total_amount_inr,
            ROUND(AVG(amount_inr), 2) AS average_transaction_amount
        FROM fact_transactions
        GROUP BY transaction_type
        ORDER BY total_amount_inr DESC;
    """,

    "QUERY 7 - TOP 10 STATES BY INVESTMENT": """
        SELECT
            state,
            COUNT(*) AS total_transactions,
            SUM(amount_inr) AS total_investment_inr
        FROM fact_transactions
        GROUP BY state
        ORDER BY total_investment_inr DESC
        LIMIT 10;
    """,

    "QUERY 8 - MONTHLY TRANSACTION TREND": """
        SELECT
            SUBSTR(transaction_date, 1, 7) AS transaction_month,
            COUNT(*) AS total_transactions,
            SUM(amount_inr) AS total_amount_inr
        FROM fact_transactions
        GROUP BY transaction_month
        ORDER BY transaction_month;
    """,

    "QUERY 9 - LATEST NAV FOR EACH FUND": """
        SELECT
            n.amfi_code,
            f.scheme_name,
            n.date,
            n.nav
        FROM fact_nav n
        JOIN dim_fund f
            ON n.amfi_code = f.amfi_code
        WHERE n.date = (
            SELECT MAX(n2.date)
            FROM fact_nav n2
            WHERE n2.amfi_code = n.amfi_code
        )
        ORDER BY n.nav DESC;
    """,

    "QUERY 10 - FUND HOUSE-WISE TOTAL AUM": """
        SELECT
            fund_house,
            MAX(date) AS latest_available_date,
            ROUND(MAX(aum_lakh_crore), 2) AS latest_aum_lakh_crore,
            MAX(aum_crore) AS latest_aum_crore,
            MAX(num_schemes) AS number_of_schemes
        FROM fact_aum
        GROUP BY fund_house
        ORDER BY latest_aum_crore DESC;
    """
}


# ==========================================
# RUN QUERIES AND SAVE RESULTS
# ==========================================

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:

    file.write(
        "BLUESTOCK MUTUAL FUND ANALYTICS PLATFORM\n"
    )

    file.write(
        "DAY 2 - SQL ANALYTICAL QUERY RESULTS\n"
    )

    file.write(
        "=" * 60 + "\n\n"
    )

    for query_name, sql_query in queries.items():

        print(query_name)

        file.write(query_name + "\n")
        file.write("-" * 60 + "\n")

        try:

            result = pd.read_sql_query(
                sql_query,
                conn
            )

            print(
                f"SUCCESS - {len(result)} rows returned\n"
            )

            file.write(
                result.to_string(index=False)
            )

            file.write(
                "\n\n"
            )

        except Exception as error:

            print(
                f"ERROR: {error}\n"
            )

            file.write(
                f"ERROR: {error}\n\n"
            )


# ==========================================
# CLOSE DATABASE
# ==========================================

conn.close()

print("===== ALL QUERIES COMPLETED =====")
print(
    f"Results saved to: {OUTPUT_FILE}"
)