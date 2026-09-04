import pandas as pd
from pathlib import Path

# ==========================================
# PATH CONFIGURATION
# ==========================================

RAW_FOLDER = Path("data/raw")
PROCESSED_FOLDER = Path("data/processed")

PROCESSED_FOLDER.mkdir(parents=True, exist_ok=True)

print("\n===== BLUESTOCK DATA CLEANING STARTED =====\n")


# ==========================================
# HELPER FUNCTION
# ==========================================

def clean_basic_dataframe(df):
    """
    Basic cleaning applied to all datasets.
    """

    # Remove completely empty rows
    df = df.dropna(how="all")

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Convert date columns
    for column in df.columns:
        if "date" in column.lower():
            df[column] = pd.to_datetime(
                df[column],
                errors="coerce"
            )

    return df


# ==========================================
# 1. FUND MASTER CLEANING
# ==========================================

print("1. Cleaning Fund Master...")

fund_master_file = RAW_FOLDER / "1788499983024-b042c300-01_fund_master.csv"

fund_master = pd.read_csv(fund_master_file)

original_rows = len(fund_master)

fund_master = clean_basic_dataframe(fund_master)

fund_master.to_csv(
    PROCESSED_FOLDER / "fund_master_cleaned.csv",
    index=False
)

print("Original rows:", original_rows)
print("Cleaned rows:", len(fund_master))
print("Saved: fund_master_cleaned.csv\n")


# ==========================================
# 2. NAV HISTORY CLEANING
# ==========================================

print("2. Cleaning NAV History...")

nav_file = RAW_FOLDER / "1788499983331-4389156d-02_nav_history.csv"

nav = pd.read_csv(nav_file)

original_rows = len(nav)

# Convert date
if "date" in nav.columns:
    nav["date"] = pd.to_datetime(
        nav["date"],
        errors="coerce"
    )

# Sort by AMFI code and date
if "amfi_code" in nav.columns and "date" in nav.columns:
    nav = nav.sort_values(
        by=["amfi_code", "date"]
    )

# Remove duplicates
nav = nav.drop_duplicates()

# Convert NAV to numeric
if "nav" in nav.columns:

    nav["nav"] = pd.to_numeric(
        nav["nav"],
        errors="coerce"
    )

    # Forward fill missing NAV values
    if "amfi_code" in nav.columns:
        nav["nav"] = (
            nav.groupby("amfi_code")["nav"]
            .ffill()
        )

    # Remove invalid NAV values
    nav = nav[nav["nav"] > 0]

# Remove rows with invalid dates
if "date" in nav.columns:
    nav = nav.dropna(subset=["date"])

nav.to_csv(
    PROCESSED_FOLDER / "nav_history_cleaned.csv",
    index=False
)

print("Original rows:", original_rows)
print("Cleaned rows:", len(nav))
print("Saved: nav_history_cleaned.csv\n")


# ==========================================
# 3. AUM BY FUND HOUSE CLEANING
# ==========================================

print("3. Cleaning AUM By Fund House...")

aum_file = RAW_FOLDER / "1788499984134-b0cbf625-03_aum_by_fund_house.csv"

aum = pd.read_csv(aum_file)

original_rows = len(aum)

aum = clean_basic_dataframe(aum)

aum.to_csv(
    PROCESSED_FOLDER / "aum_by_fund_house_cleaned.csv",
    index=False
)

print("Original rows:", original_rows)
print("Cleaned rows:", len(aum))
print("Saved: aum_by_fund_house_cleaned.csv\n")


# ==========================================
# 4. MONTHLY SIP INFLOWS CLEANING
# ==========================================

print("4. Cleaning Monthly SIP Inflows...")

sip_file = RAW_FOLDER / "1788499984405-d702a6c6-04_monthly_sip_inflows.csv"

sip = pd.read_csv(sip_file)

original_rows = len(sip)

sip = clean_basic_dataframe(sip)

# Keep yoy_growth_pct missing values because
# first 12 months may not have previous-year data.

sip.to_csv(
    PROCESSED_FOLDER / "monthly_sip_inflows_cleaned.csv",
    index=False
)

print("Original rows:", original_rows)
print("Cleaned rows:", len(sip))
print("Saved: monthly_sip_inflows_cleaned.csv\n")


# ==========================================
# 5. CATEGORY INFLOWS CLEANING
# ==========================================

print("5. Cleaning Category Inflows...")

category_file = RAW_FOLDER / "1788499984721-4b860901-05_category_inflows.csv"

category = pd.read_csv(category_file)

original_rows = len(category)

category = clean_basic_dataframe(category)

category.to_csv(
    PROCESSED_FOLDER / "category_inflows_cleaned.csv",
    index=False
)

print("Original rows:", original_rows)
print("Cleaned rows:", len(category))
print("Saved: category_inflows_cleaned.csv\n")


# ==========================================
# 6. INDUSTRY FOLIO COUNT CLEANING
# ==========================================

print("6. Cleaning Industry Folio Count...")

folio_file = RAW_FOLDER / "1788499985036-da4a0c4a-06_industry_folio_count.csv"

folio = pd.read_csv(folio_file)

original_rows = len(folio)

folio = clean_basic_dataframe(folio)

folio.to_csv(
    PROCESSED_FOLDER / "industry_folio_count_cleaned.csv",
    index=False
)

print("Original rows:", original_rows)
print("Cleaned rows:", len(folio))
print("Saved: industry_folio_count_cleaned.csv\n")


# ==========================================
# 7. SCHEME PERFORMANCE CLEANING
# ==========================================

print("7. Cleaning Scheme Performance...")

performance_file = (
    RAW_FOLDER /
    "1788499985420-bb134abf-07_scheme_performance.csv"
)

performance = pd.read_csv(performance_file)

original_rows = len(performance)

performance = clean_basic_dataframe(performance)

# Convert numerical performance columns
for column in performance.columns:

    column_name = column.lower()

    if (
        "return" in column_name
        or "ratio" in column_name
        or "performance" in column_name
    ):

        performance[column] = pd.to_numeric(
            performance[column],
            errors="coerce"
        )

# Validate expense ratio
if "expense_ratio_pct" in performance.columns:

    invalid_expense = performance[
        (performance["expense_ratio_pct"] < 0.1)
        | (performance["expense_ratio_pct"] > 2.5)
    ]

    print(
        "Invalid expense ratio values:",
        len(invalid_expense)
    )

performance.to_csv(
    PROCESSED_FOLDER / "scheme_performance_cleaned.csv",
    index=False
)

print("Original rows:", original_rows)
print("Cleaned rows:", len(performance))
print("Saved: scheme_performance_cleaned.csv\n")


# ==========================================
# 8. INVESTOR TRANSACTIONS CLEANING
# ==========================================

print("8. Cleaning Investor Transactions...")

transaction_file = (
    RAW_FOLDER /
    "1788499980509-304c1255-08_investor_transactions.csv"
)

transactions = pd.read_csv(transaction_file)

original_rows = len(transactions)

# Convert date columns
for column in transactions.columns:

    if "date" in column.lower():

        transactions[column] = pd.to_datetime(
            transactions[column],
            errors="coerce"
        )

# Standardize transaction type
if "transaction_type" in transactions.columns:

    transactions["transaction_type"] = (
        transactions["transaction_type"]
        .astype(str)
        .str.strip()
        .str.title()
    )

# Convert amount columns to numeric
for column in transactions.columns:

    if "amount" in column.lower():

        transactions[column] = pd.to_numeric(
            transactions[column],
            errors="coerce"
        )

        # Remove invalid or negative amounts
        transactions = transactions[
            transactions[column] > 0
        ]

# Remove duplicates
transactions = transactions.drop_duplicates()

# Remove completely empty rows
transactions = transactions.dropna(how="all")

transactions.to_csv(
    PROCESSED_FOLDER / "investor_transactions_cleaned.csv",
    index=False
)

print("Original rows:", original_rows)
print("Cleaned rows:", len(transactions))
print("Saved: investor_transactions_cleaned.csv\n")


# ==========================================
# 9. PORTFOLIO HOLDINGS CLEANING
# ==========================================

print("9. Cleaning Portfolio Holdings...")

portfolio_file = (
    RAW_FOLDER /
    "1788499982117-e3d6ab98-09_portfolio_holdings.csv"
)

portfolio = pd.read_csv(portfolio_file)

original_rows = len(portfolio)

portfolio = clean_basic_dataframe(portfolio)

portfolio.to_csv(
    PROCESSED_FOLDER / "portfolio_holdings_cleaned.csv",
    index=False
)

print("Original rows:", original_rows)
print("Cleaned rows:", len(portfolio))
print("Saved: portfolio_holdings_cleaned.csv\n")


# ==========================================
# 10. BENCHMARK INDICES CLEANING
# ==========================================

print("10. Cleaning Benchmark Indices...")

benchmark_file = (
    RAW_FOLDER /
    "1788499982615-f9647ab2-10_benchmark_indices.csv"
)

benchmark = pd.read_csv(benchmark_file)

original_rows = len(benchmark)

benchmark = clean_basic_dataframe(benchmark)

benchmark.to_csv(
    PROCESSED_FOLDER / "benchmark_indices_cleaned.csv",
    index=False
)

print("Original rows:", original_rows)
print("Cleaned rows:", len(benchmark))
print("Saved: benchmark_indices_cleaned.csv\n")


# ==========================================
# COMPLETION
# ==========================================

print("===== DATA CLEANING COMPLETED =====\n")

print("Processed files created:")

for file in sorted(PROCESSED_FOLDER.glob("*.csv")):
    print("-", file.name)

print(
    f"\nTotal processed CSV files: "
    f"{len(list(PROCESSED_FOLDER.glob('*.csv')))}"
)